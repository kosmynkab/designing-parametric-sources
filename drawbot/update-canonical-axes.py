import json
import os


scriptFolder = os.path.dirname(os.path.abspath(__file__))
repositoryFolder = os.path.dirname(scriptFolder)
dataFolder = os.path.join(repositoryFolder, "src", "_data")

canonicalAxesPath = os.path.join(dataFolder, "canonical-axes.json")
specimensPath = os.path.join(dataFolder, "specimens.json")


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


with open(canonicalAxesPath, "r", encoding="utf-8") as file:
    canonicalAxes = json.load(file)

with open(specimensPath, "r", encoding="utf-8") as file:
    specimenData = json.load(file)

updatedCount = 0

for specimen in specimenData["specimens"]:
    projectId = specimen["project"]
    lookup = canonical_axis_lookup(canonicalAxes, projectId)

    canonicalAxis = lookup.get(specimen["axis"])
    specimen["canonical_axis"] = canonicalAxis

    if canonicalAxis is not None:
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