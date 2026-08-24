# Export Glyph Meme PNGs — cached-source version

import os
import re
import sys
import json
import time

import drawBot as DB
from fontParts.world import OpenFont
from fontTools.designspaceLib import DesignSpaceDocument

# ---------------------------------------------------------------------------
# SETTINGS

baseFolder = os.path.dirname(os.getcwd())

siteSourceFolder = os.path.join(baseFolder, "src")
outputFolder = os.path.join(siteSourceFolder, "imgs")
dataFolder = os.path.join(siteSourceFolder, "_data")
glyphsPath = os.path.join(dataFolder, "glyphs.json")
specimensPath = os.path.join(dataFolder, "specimens.json")
parentAxesPath = os.path.join(dataFolder, "parent-axes.json")

scriptFolder = os.path.dirname(os.path.abspath(__file__))
localSettingsPath = os.path.join(scriptFolder, "local-settings.json")

with open(localSettingsPath, "r", encoding="utf-8") as file:
    localSettings = json.load(file)

sourceProjectFolder = localSettings["sourceProjectFolder"]
toolsFolder = os.path.join(sourceProjectFolder, "Tools")

if toolsFolder not in sys.path:
    sys.path.insert(0, toolsFolder)

from controller import AmstelvarA2Controller
from xTools4.modules.glyphMemeProofer import GlyphMemeProofer
from xTools4.modules.linkPoints2 import readMeasurements
from xTools4.modules.sys import timer
from collections import defaultdict
from time import perf_counter

subFamilies = ["Roman", "Italic"]
includeGRAD = True

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
        f"{source_label(sourceName, availableSourceNames)}.png"
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
    pngPath,
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
        "image": os.path.relpath(pngPath, siteSourceFolder),
        "group": glyphMetadata.get("group"),
        "tags": glyphMetadata.get("tags", []),
    }

    if sourceLabel.endswith("min"):
        record["instance"] = "min"
    elif sourceLabel.endswith("max"):
        record["instance"] = "max"

    return record


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

        pngPath = os.path.join(
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
        DB.saveImage(pngPath, imageResolution=144)
        timings["save PNG"] += perf_counter() - start
        counts["save PNG"] += 1

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
                pngPath,
                glyphs,
                measurements,
                parentAxisLookup,
            )
        )

        print(f"saved {pngPath}")


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
    "save PNG",
    "end drawing",
):
    total = timings[name]
    count = counts[name]
    average = total / count if count else 0
    print(f"{name:18} {total:7.2f}s total   {average:0.4f}s/image   ({count} calls)")

timer(start, end)