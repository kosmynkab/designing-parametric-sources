import fs from "node:fs";

const projectNames = {
  "amstelvar-a2": "Amstelvar Avar2"
};

const source = JSON.parse(
  fs.readFileSync(
    new URL("./canonical-axes.json", import.meta.url),
    "utf8"
  )
);

const byId = Object.fromEntries(
  Object.entries(source.projects).map(([projectId, project]) => [
    projectId,
    {
      id: projectId,
      name: projectNames[projectId] || projectId,
      canonicalAxes: project.canonical_axes
    }
  ])
);

export default {
  byId
};