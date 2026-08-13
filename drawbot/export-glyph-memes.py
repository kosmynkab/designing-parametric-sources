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
                
#glyphNames = ["H", "O", "G", "V", "E", "T", "o", "v", "one", "zero", "n", "r", "c"]
with open(glyphsPath, "r", encoding="utf-8") as f:
    glyphs = json.load(f)["glyphs"]

glyphNames = list(glyphs)

# sourceNames = ["XOUC4", "XOUC310"]
sourceNames = None

# Prefer general parent-axis names such as XOPQ rather than Amstelvar's
# class-specific source names such as XOUC/XOLC.
useParentAxisNames = True

# ---------------------------------------------------------------------------
# IMPLEMENTATION

# Rename into Parent Axis name
PARENT_AXIS_GROUPS = {
    # Optical-size / contrast parameters
    "XOPQ": ("XOUC", "XOLC", "XOFI", "XOET"),
    "YOPQ": ("YOUC", "YOLC", "YOFI", "YOET"),

    # Stem / proportion parameters
    "XTRA": ("XTUC", "XTUR", "XTUD", "XTUA", "XTLC", "XTLR", "XTLD", "XTLA", "XTFI", "XTET"),
    "XSHA": ("XSHU", "XSHL", "XSHF"),
    "YSHA": ("YSHU", "YSHL", "YSHF"),
    "XSVA": ("XSVU", "XSVL", "XSVF"),
    "YSVA": ("YSVU", "YSVL", "YSVF"),
    "XVAA": ("XVAU",),
    "YTRA": ("YTUC", "YTLC", "YTFI"),

    # Counter / contrast parameters
    "XTEQ": ("XQUC", "XQLC", "XQFI"),
    "YTEQ": ("YQUC", "YQLC", "YQFI"),
    
    # Spacing parameters
    "XTSP": ("XUCS", "XUCD", "XUCR", "XLCS", "XLCD", "XLCR", "XFIR", "XETS"),
}

PARENT_AXIS_NAMES = {
    childTag: parentTag
    for parentTag, childTags in PARENT_AXIS_GROUPS.items()
    for childTag in childTags
}


def split_source_name(sourceName):
    match = re.fullmatch(r"([A-Z]+)(-?\d+)", sourceName)
    if match is None:
        return sourceName, None
    return match.group(1), int(match.group(2))

# Turn XOUC4/XOUC310 or XOLC4/XOLC293 into XOPQmin/XOPQmax
def source_label(sourceName, availableSourceNames):

    tag, value = split_source_name(sourceName)
    values = [
        otherValue
        for name in availableSourceNames
        for otherTag, otherValue in [split_source_name(name)]
        if otherTag == tag and otherValue is not None
    ]

    axisName = PARENT_AXIS_NAMES.get(tag, tag) if useParentAxisNames else tag
    if value is not None and len(set(values)) > 1:
        if value == min(values):
            return f"{axisName}min"
        if value == max(values):
            return f"{axisName}max"
    return sourceName


def file_name(familyName, glyphName, sourceName, availableSourceNames):
    return (
        f"{familyName}-{subFamily}_{glyphName}_"
        f"{source_label(sourceName, availableSourceNames)}.png"
    )

def specimen_record(glyphName, styleName, sourceName, availableSourceNames, pngPath, glyphs):
    sourceTag, _ = split_source_name(sourceName)
    sourceLabel = source_label(sourceName, availableSourceNames)
    glyphMetadata = glyphs.get(glyphName, {})

    record = {
        "id": f"amstelvar-{sourceLabel.lower()}-{glyphName}-{styleName.lower()}",
        "glyph": glyphName,
        "axis": PARENT_AXIS_NAMES.get(sourceTag, sourceTag),
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

def export_glyph(glyphName, designspacePath, familyName, styleName, glyphs, specimens):
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

    glyphFolder = os.path.join(outputFolder, category)
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
                styleName,
                sourceName,
                availableSourceNames,
                pngPath,
                glyphs,
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

    for glyphName in glyphNames:
        export_glyph(
            glyphName,
            controller.designspacePath,
            controller.familyName,
            subFamily,
            glyphs,
            specimens,
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