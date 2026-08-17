import canonicalAxes from "./canonicalAxes.js";
import projectAxisMappings from "./projectAxisMappings.js";
import projectDesignAxes from "./projectDesignAxes.js";

function canonicalAxisUrl(axis) {
  return `/reference/axes/${axis.id}/`;
}

function designAxisUrl(axis) {
  return `/reference/design-axes/${axis.tag.toLowerCase()}/`;
}

export default function referenceTree() {
  const designAxes = projectDesignAxes();

  return {
    canonicalAxes: canonicalAxes.all.map((axis) => ({
      ...axis,
      url: canonicalAxisUrl(axis)
    })),

    projects: Object.values(projectAxisMappings.byId)
      .map((project) => ({
        ...project,
        designAxes: designAxes.all
          .filter((axis) => axis.project === project.id)
          .sort((first, second) => first.tag.localeCompare(second.tag))
          .map((axis) => ({
            ...axis,
            url: designAxisUrl(axis)
          }))
      }))
      .filter((project) => project.designAxes.length)
  };
}