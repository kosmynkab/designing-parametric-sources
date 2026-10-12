# Export Glyph Meme SVGs — cached-source version
# Run in the same DrawBot/RoboFont environment as export-glyph-memes_new.py.
# Uses the same glyph/style/source selections, but keeps PNG assets and their
# manifest untouched. Each SVG embeds a subset of Roboto for portable labels.

import os
import re
import sys
import json
import time
import base64
import io
import xml.etree.ElementTree as ET
from functools import lru_cache

from fontTools import subset
from fontTools.ttLib import TTFont

import drawBot as DB
from fontParts.world import OpenFont
from fontTools.designspaceLib import DesignSpaceDocument

# ---------------------------------------------------------------------------
# SETTINGS

scriptFolder = os.path.dirname(os.path.abspath(__file__))
baseFolder = os.path.dirname(scriptFolder)

siteSourceFolder = os.path.join(baseFolder, "src")
outputFolder = os.path.join(siteSourceFolder, "imgs-svg")
dataFolder = os.path.join(siteSourceFolder, "_data")
glyphsPath = os.path.join(dataFolder, "glyphs.json")
specimensPath = os.path.join(dataFolder, "specimens.json")
parentAxesPath = os.path.join(dataFolder, "parent-axes.json")

localSettingsPath = os.path.join(scriptFolder, "local-settings.json")

with open(localSettingsPath, "r", encoding="utf-8") as file:
    localSettings = json.load(file)

sourceProjectFolder = localSettings["sourceProjectFolder"]
toolsFolder = os.path.join(sourceProjectFolder, "Tools")

if toolsFolder not in sys.path:
    sys.path.insert(0, toolsFolder)

from controller import AmstelvarA2Controller
from xTools4.modules.glyphMemeProofer import (
    GlyphMemeProofer, checkCompatibility, checkEquality,
    colorCheckEqual, colorCheckTrue, colorCheckFalse,
)
from xTools4.modules.linkPoints2 import readMeasurements
from xTools4.modules.measurements import Measurement
from xTools4.modules.sys import timer
from collections import defaultdict
from time import perf_counter

subFamilies = ["Roman", "Italic"]
includeGRAD = True

# An installed Roboto face, or a path to a local Roboto TTF/OTF file.
# Optionally set "annotationFont" in local-settings.json to override this.
annotationFont = localSettings.get("annotationFont", "Roboto-Regular")
if not os.path.isfile(annotationFont) and annotationFont not in DB.installedFonts():
    raise RuntimeError(
        f"Annotation font {annotationFont!r} is unavailable. Install Roboto Regular "
        'or set "annotationFont" in drawbot/local-settings.json to its TTF/OTF path.'
    )
DB.font(annotationFont)
annotationFontPath = os.fspath(DB.fontFilePath())
annotationFontNumber = DB.fontFileFontNumber()

with open(glyphsPath, "r", encoding="utf-8") as file:
    glyphs = json.load(file)["glyphs"]

with open(parentAxesPath, "r", encoding="utf-8") as file:
    parentAxes = json.load(file)

glyphNames = list(glyphs)

# Set to a list of source names to export only those sources.
# Example: ["XOUC4", "XOUC310"]
sourceNames = None

timings = defaultdict(float)
counts = defaultdict(int)


def time_phase(name, callback):
    start = perf_counter()
    result = callback()
    timings[name] += perf_counter() - start
    counts[name] += 1
    return result

# ---------------------------------------------------------------------------
# HELPERS

def split_source_name(sourceName):
    match = re.fullmatch(r"([A-Z]+)(-?\d+)", sourceName)
    if match is None:
        return sourceName, None
    return match.group(1), int(match.group(2))


def project_id(familyName):
    return re.sub(
        r"(?<=[a-z])(?=[A-Z0-9])|(?<=[A-Z])(?=[A-Z][a-z])",
        "-",
        familyName,
    ).lower()


def source_label(sourceName, availableSourceNames):
    tag, value = split_source_name(sourceName)
    values = [
        otherValue
        for name in availableSourceNames
        for otherTag, otherValue in [split_source_name(name)]
        if otherTag == tag and otherValue is not None
    ]

    if value is not None and len(set(values)) > 1:
        if value == min(values):
            return f"{tag}min"
        if value == max(values):
            return f"{tag}max"

    return sourceName


def file_name(familyName, subFamily, glyphName, sourceName, availableSourceNames):
    return (
        f"{familyName}-{subFamily}_{glyphName}_"
        f"{source_label(sourceName, availableSourceNames)}.svg"
    )


def parent_axis_lookup(parentAxes, projectId):
    parentAxesByProject = (
        parentAxes["projects"]
        .get(projectId, {})
        .get("parent_axes", {})
    )

    return {
        childAxis: parentAxis
        for parentAxis, childAxes in parentAxesByProject.items()
        for childAxis in childAxes
    }


def specimen_record(
    glyphName,
    familyName,
    styleName,
    sourceName,
    availableSourceNames,
    svgPath,
    glyphs,
    measurements,
    parentAxisLookup,
):
    sourceTag, _ = split_source_name(sourceName)
    sourceLabel = source_label(sourceName, availableSourceNames)
    glyphMetadata = glyphs.get(glyphName, {})
    axisMetadata = measurements.get(sourceTag, {})
    axisGroup = axisMetadata.get("parent") or sourceTag
    projectId = project_id(familyName)

    record = {
        "id": f"{projectId}-{sourceLabel.lower()}-{glyphName}-{styleName.lower()}",
        "project": projectId,
        "glyph": glyphName,
        "axis": sourceTag,
        "parent_axis": parentAxisLookup.get(sourceTag),
        "axis_group": axisGroup,
        "axis_description": axisMetadata.get("description"),
        "style": styleName.lower(),
        "source": sourceName,
        "image": os.path.relpath(svgPath, siteSourceFolder),
        "group": glyphMetadata.get("group"),
        "tags": glyphMetadata.get("tags", []),
    }

    if sourceLabel.endswith("min"):
        record["instance"] = "min"
    elif sourceLabel.endswith("max"):
        record["instance"] = "max"

    return record



SVG_NAMESPACE = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NAMESPACE)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


@lru_cache(maxsize=128)
def annotation_font_data(characters):
    """Subset only characters used by this proof; preserve text as text."""
    font = TTFont(annotationFontPath, fontNumber=annotationFontNumber)
    try:
        options = subset.Options()
        subsetter = subset.Subsetter(options=options)
        subsetter.populate(text=characters)
        subsetter.subset(font)
        # Raw OpenType avoids an extra WOFF/Brotli dependency in RoboFont.
        font.flavor = None
        buffer = io.BytesIO()
        font.save(buffer)
        return base64.b64encode(buffer.getvalue()).decode("ascii")
    finally:
        font.close()


def embed_annotation_font(svgPath):
    """Make SVG <img> previews independent of locally installed fonts."""
    tree = ET.parse(svgPath)
    root = tree.getroot()
    textNodes = list(root.iter(f"{{{SVG_NAMESPACE}}}text"))
    if textNodes:
        characters = "".join(sorted(set(
            "".join("".join(node.itertext()) for node in textNodes)
        )))
        data = annotation_font_data(characters)
        defs = ET.Element(f"{{{SVG_NAMESPACE}}}defs")
        style = ET.SubElement(defs, f"{{{SVG_NAMESPACE}}}style", type="text/css")
        style.text = (
            "@font-face{font-family:ProofRoboto;"
            f"src:url(data:font/opentype;base64,{data}) format('opentype');"
            "font-style:normal;font-weight:400;}"
        )
        root.insert(0, defs)
        for textNode in textNodes:
            for node in textNode.iter():
                if node.tag in {f"{{{SVG_NAMESPACE}}}text", f"{{{SVG_NAMESPACE}}}tspan"}:
                    node.set("font-family", "ProofRoboto")
    tree.write(svgPath, encoding="utf-8", xml_declaration=True)


def report_sizes(specimens):
    svgBytes = pngBytes = matchedSvgBytes = matchedCount = 0
    for record in specimens:
        svgPath = os.path.join(siteSourceFolder, record["image"])
        size = os.path.getsize(svgPath)
        svgBytes += size
        relative = os.path.relpath(svgPath, outputFolder)
        pngPath = os.path.join(siteSourceFolder, "imgs", os.path.splitext(relative)[0] + ".png")
        if os.path.isfile(pngPath):
            pngBytes += os.path.getsize(pngPath)
            matchedSvgBytes += size
            matchedCount += 1
    print(f"\nSVG export: {len(specimens)} images, {svgBytes / 1_000_000:.2f} MB")
    if pngBytes:
        saving = 100 * (1 - matchedSvgBytes / pngBytes)
        print(
            f"Matched comparison ({matchedCount} images): "
            f"PNG {pngBytes / 1_000_000:.2f} MB → "
            f"SVG {matchedSvgBytes / 1_000_000:.2f} MB ({saving:.1f}% smaller)"
        )
    else:
        print("No matching PNGs found for size comparison.")

# ---------------------------------------------------------------------------
# CACHED FONT ACCESS

class FontCache:
    """Open each UFO at most once for a complete subfamily export."""

    def __init__(self):
        self._fonts = {}

    def get(self, path):
        path = os.path.abspath(os.fspath(path))
        font = self._fonts.get(path)

        if font is None:
            font = OpenFont(path, showInterface=False)
            self._fonts[path] = font

        return font


class CachedGlyphMemeProofer(GlyphMemeProofer):
    """
    Preserve GlyphMemeProofer's drawing behavior, while sharing already-loaded
    designspace, measurement data, default font, and source fonts.
    """

    def __init__(self, glyphName, designspace, measurementsData, fontCache):
        self.glyphName = glyphName
        self.designspace = designspace
        self._measurementsData = measurementsData
        self._fontCache = fontCache

    @property
    def glyphMeasurements(self):
        return self._measurementsData["glyphs"].get(self.glyphName)

    @property
    def parametricGlyphs(self):
        glyphsBySource = {}

        for srcName, srcPath in self.parametricSources.items():
            font = self._fontCache.get(srcPath)
            glyphsBySource[srcName] = font[self.glyphName]

        return glyphsBySource

    @property
    def defaultFont(self):
        return self._fontCache.get(self.designspace.default.path)


    def _drawMeasurements(self, glyph):
        """Position individual cells; SVG text does not preserve tab stops."""
        panelX = self.canvasWidth + self.captionSize
        panelW = self.panelWidth - self.captionSize * 2
        rowHeight = self.captionSize * 1.2
        headerY = self.canvasHeight - self.captionSize * 2
        # Fixed column anchors within the panel: name left, numbers right.
        columns = (0, panelW * 0.32, panelW * 0.47,
                   panelW * 0.73, panelW)

        def draw_cell(text, column, y, color):
            DB.fill(*color)
            DB.text(str(text), (panelX + columns[column], y),
                    align="left" if column == 0 else "right")

        with DB.savedState():
            DB.font(self.captionFont)
            DB.fontSize(self.captionSize)
            DB.stroke(None)
            for column, label in enumerate(("name", "p1", "p2", "units", "scale")):
                draw_cell(label, column, headerY, self.captionColor)

            with DB.savedState():
                DB.stroke(*self.captionColor)
                DB.strokeWidth(0.5)
                DB.lineDash(None)
                lineY = headerY - rowHeight * 0.5
                DB.line((panelX, lineY), (panelX + panelW, lineY))

            for row, (points, metadata) in enumerate(self.glyphMeasurements.items()):
                pt1, pt2 = points.split()
                measurement = Measurement(
                    metadata["name"], metadata["direction"],
                    glyph.name, pt1, glyph.name, pt2,
                )
                value = measurement.measure(glyph.font, italicCorrection=True)
                defaultValue = measurement.measure(self.defaultFont, italicCorrection=True)
                scale = value / defaultValue if defaultValue != 0 else None
                if scale is None:
                    color = self.captionColor
                elif scale == 1:
                    color = colorCheckEqual
                elif 1 - self.measurementsThreshold < scale < 1 + self.measurementsThreshold:
                    color = colorCheckTrue
                else:
                    color = colorCheckFalse

                y = headerY - (row + 1.5) * rowHeight
                draw_cell(metadata["name"], 0, y, color)
                for column, text in enumerate((pt1, pt2, value), start=1):
                    draw_cell(text, column, y, self.captionColor)
                draw_cell("–" if scale is None else f"{scale:.2f}", 4, y, color)

    def _drawValidation(self, glyph):

        defaultGlyph = self.defaultFont[glyph.name]

        checkResults = {
            'compatibility' : checkCompatibility(glyph, defaultGlyph),
            'equality'      : checkEquality(glyph, defaultGlyph),
        }

        T = DB.FormattedString()
        T.font(self.captionFont)
        T.fontSize(self.captionSize)
        T.stroke(None)
        T.fill(*self.captionColor)

        for checkName, isEqual in checkResults['equality'].items():
            isCompatible = checkResults['compatibility'].get(checkName)
            if isCompatible and isEqual:
                color = colorCheckEqual
            elif isCompatible or isEqual:
                color = colorCheckTrue
            else:
                color = colorCheckFalse

            T.fill(*color)
            T.append(f'{checkName[0].upper()} ')

        vX = self.canvasWidth + self.captionSize
        vY = self.captionSize

        DB.text(T, (vX, vY))

# ---------------------------------------------------------------------------
# EXPORT

def export_glyph(
    glyphName,
    designspace,
    familyName,
    styleName,
    glyphs,
    specimens,
    measurements,
    measurementsData,
    parentAxisLookup,
    fontCache,
):
    proofer = CachedGlyphMemeProofer(
        glyphName,
        designspace,
        measurementsData,
        fontCache,
    )

    if proofer.glyphMeasurements is None:
        print(f"skipped /{glyphName}: no parametric measurements")
        return

    proofer.captionFont = annotationFont
    proofer.anchorsDraw = True
    glyphsBySource = dict(proofer.parametricGlyphs)

    if includeGRAD:
        for source in designspace.sources:
            if source.styleName.startswith("GRAD"):
                font = fontCache.get(source.path)

                if glyphName in font:
                    glyphsBySource[source.styleName] = font[glyphName]

    if not glyphsBySource:
        print(f"skipped /{glyphName}: no parametric Glyph Meme sources")
        return

    availableSourceNames = tuple(glyphsBySource)
    referenceGlyph = proofer.defaultFont[glyphName]

    if referenceGlyph.unicode is None:
        category = "other"
    else:
        character = chr(referenceGlyph.unicode)

        if character.isupper():
            category = "uc"
        elif character.islower():
            category = "lc"
        else:
            category = "other"

    projectId = project_id(familyName)
    glyphFolder = os.path.join(outputFolder, projectId, category)
    os.makedirs(glyphFolder, exist_ok=True)

    for sourceName, glyph in glyphsBySource.items():
        if sourceNames is not None and sourceName not in sourceNames:
            continue

        svgPath = os.path.join(
            glyphFolder,
            file_name(
                familyName,
                styleName,
                glyphName,
                sourceName,
                availableSourceNames,
            ),
        )

        start = perf_counter()
        DB.newDrawing()
        timings["new drawing"] += perf_counter() - start
        counts["new drawing"] += 1

        start = perf_counter()
        proofer.drawGlyph(glyph, sourceName)
        timings["draw glyph meme"] += perf_counter() - start
        counts["draw glyph meme"] += 1

        start = perf_counter()
        DB.saveImage(svgPath)
        embed_annotation_font(svgPath)
        timings["save SVG"] += perf_counter() - start
        counts["save SVG"] += 1

        start = perf_counter()
        DB.endDrawing()
        timings["end drawing"] += perf_counter() - start
        counts["end drawing"] += 1

        specimens.append(
            specimen_record(
                glyphName,
                familyName,
                styleName,
                sourceName,
                availableSourceNames,
                svgPath,
                glyphs,
                measurements,
                parentAxisLookup,
            )
        )

        print(f"saved {svgPath}")


# ---------------------------------------------------------------------------
# MAIN

os.makedirs(outputFolder, exist_ok=True)
os.makedirs(dataFolder, exist_ok=True)

specimens = []
start = time.time()

for subFamily in subFamilies:
    controller = AmstelvarA2Controller(
        sourceProjectFolder,
        "AmstelvarA2",
        subFamily,
    )

    designspace = DesignSpaceDocument()
    designspace.read(controller.designspacePath)

    measurementsData = readMeasurements(controller.measurementsPath)
    measurements = measurementsData["font"]

    projectId = project_id(controller.familyName)
    parentAxisLookup = parent_axis_lookup(parentAxes, projectId)
    fontCache = FontCache()

    for glyphName in glyphNames:
        export_glyph(
            glyphName,
            designspace,
            controller.familyName,
            subFamily,
            glyphs,
            specimens,
            measurements,
            measurementsData,
            parentAxisLookup,
            fontCache,
        )

with open(specimensPath, "w", encoding="utf-8") as file:
    json.dump(
        {"schema_version": "0.1", "specimens": specimens},
        file,
        indent=2,
        ensure_ascii=False,
    )
    file.write("\n")

print(f"saved {specimensPath}")

end = time.time()

print("\n--- Export timing report ---")

for name in (
    "new drawing",
    "draw glyph meme",
    "save SVG",
    "end drawing",
):
    total = timings[name]
    count = counts[name]
    average = total / count if count else 0
    print(f"{name:18} {total:7.2f}s total   {average:0.4f}s/image   ({count} calls)")

report_sizes(specimens)
timer(start, end)
