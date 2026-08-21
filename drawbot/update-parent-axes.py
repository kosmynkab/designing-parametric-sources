import json
import os


scriptFolder = os.path.dirname(os.path.abspath(__file__))
repositoryFolder = os.path.dirname(scriptFolder)
dataFolder = os.path.join(repositoryFolder, "src", "_data")

parentAxesPath = os.path.join(dataFolder, "parent-axes.json")
specimensPath = os.path.join(dataFolder, "specimens.json")


def parent_axis_lookup(parentAxes, projectId):
    parentAxesByProject = (
        parentAxes["projects"]
        .get(projectId, {})
        .get("parent_axes", {})
    )

    return {
        designAxis: parentAxis
        for parentAxis, designAxes in parentAxesByProject.items()
        for designAxis in designAxes
    }


with open(parentAxesPath, "r", encoding="utf-8") as file:
    parentAxes = json.load(file)

with open(specimensPath, "r", encoding="utf-8") as file:
    specimenData = json.load(file)

updatedCount = 0

for specimen in specimenData["specimens"]:
    projectId = specimen["project"]
    lookup = parent_axis_lookup(parentAxes, projectId)

    parentAxis = lookup.get(specimen["axis"])
    specimen["parent_axis"] = parentAxis

    if parentAxis is not None:
        updatedCount += 1

with open(specimensPath, "w", encoding="utf-8") as file:
    json.dump(
        specimenData,
        file,
        indent=2,
        ensure_ascii=False,
    )
    file.write("\n")

print(f"updated {updatedCount} specimen records")