# Export Glyph Meme PNGs

import os
import re
import sys
import drawBot as DB
import json
import time

# ---------------------------------------------------------------------------
# SETTINGS

baseFolder = os.path.dirname(os.getcwd())

siteSourceFolder = os.path.join(baseFolder, "src")
outputFolder = os.path.join(baseFolder, "src", "imgs")
dataFolder = os.path.join(baseFolder, "src", "_data")
glyphsPath = os.path.join(dataFolder, "glyphs.json")
specimensPath = os.path.join(dataFolder, "specimens.json")
canonicalAxesPath = os.path.join(dataFolder, "canonical-axes.json")

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
from xTools4.modules.sys import timer


subFamilies = ["Roman", "Italic"]
includeGRAD = True
                
with open(glyphsPath, "r", encoding="utf-8") as f:
    glyphs = json.load(f)["glyphs"]

with open(canonicalAxesPath, "r", encoding="utf-8") as file:
    canonicalAxes = json.load(file)

glyphNames = list(glyphs)

# sourceNames = ["XOUC4", "XOUC310"]
sourceNames = None


# ---------------------------------------------------------------------------
# IMPLEMENTATION

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

# Turn XOUC4/XOUC310 into XOUCmin/XOUCmax
def source_label(sourceName, availableSourceNames):

    tag, value = split_source_name(sourceName)
    values = [
        otherValue
        for name in availableSourceNames
        for otherTag, otherValue in [split_source_name(name)]
        if otherTag == tag and otherValue is not None
    ]

    axisName = tag
    if value is not None and len(set(values)) > 1:
        if value == min(values):
            return f"{axisName}min"
        if value == max(values):
            return f"{axisName}max"
    return sourceName

def canonical_axis_lookup(canonicalAxes, projectId):
    canonicalAxesByProject = (
        canonicalAxes["projects"]
        .get(projectId, {})
        .get("canonical_axes", {})
    )

    return {
        designAxis: canonicalAxis
        for canonicalAxis, designAxes in canonicalAxesByProject.items()
        for designAxis in designAxes
    }

def file_name(familyName, glyphName, sourceName, availableSourceNames):
    return (
        f"{familyName}-{subFamily}_{glyphName}_"
        f"{source_label(sourceName, availableSourceNames)}.png"
    )

def specimen_record(glyphName, familyName, styleName, sourceName, availableSourceNames, pngPath, glyphs, measurements, canonicalAxisLookup):
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
        "canonical_axis": canonicalAxisLookup.get(sourceTag),
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

def export_glyph(glyphName, designspacePath, familyName, styleName, glyphs, specimens, measurements, canonicalAxisLookup):
    proofer = GlyphMemeProofer(glyphName, designspacePath)
    
    if proofer.glyphMeasurements is None:
        print(f"skipped /{glyphName}: no parametric measurements")
        return
        
    exportScale = 2.0

    proofer.canvasWidth *= exportScale
    proofer.canvasHeight *= exportScale
    proofer.panelWidth *= exportScale
    proofer.glyphScale *= exportScale
    proofer.captionSize *= exportScale
    proofer.pointLabelsSize *= exportScale
    proofer.anchorsDraw = True

    glyphsBySource = dict(proofer.parametricGlyphs)

    if includeGRAD:
        for source in proofer.designspace.sources:
            if source.styleName.startswith("GRAD"):
                font = OpenFont(source.path, showInterface=False)
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
            file_name(familyName, glyphName, sourceName, availableSourceNames),
        )

        DB.newDrawing()
        proofer.drawGlyph(glyph, sourceName)
        DB.saveImage(pngPath)
        DB.endDrawing()

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
                canonicalAxisLookup,
            )
        )

        print(f"saved {pngPath}")

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
    with open(controller.measurementsPath, "r", encoding="utf-8") as file:
        measurements = json.load(file)["font"]

    projectId = project_id(controller.familyName)
    canonicalAxisLookup = canonical_axis_lookup(
        canonicalAxes,
        projectId,
    )

    for glyphName in glyphNames:
        export_glyph(
            glyphName,
            controller.designspacePath,
            controller.familyName,
            subFamily,
            glyphs,
            specimens,
            measurements,
            canonicalAxisLookup,
        )

with open(specimensPath, "w", encoding="utf-8") as f:
    json.dump(
        {"schema_version": "0.1", "specimens": specimens},
        f,
        indent=2,
        ensure_ascii=False,
    )
    f.write("\n")

print(f"saved {specimensPath}")

end = time.time()
timer(start, end)