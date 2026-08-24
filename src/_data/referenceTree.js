import parentAxes from "./parentAxes.js";
import projectAxisMappings from "./projectAxisMappings.js";
import projectChildAxes from "./projectChildAxes.js";

function parentAxisUrl(axis) {
  return `/reference/axes/${axis.id}/`;
}

function childAxisUrl(axis) {
  return `/reference/child-axes/${axis.tag.toLowerCase()}/`;
}

export default function referenceTree() {
  const childAxes = projectChildAxes();

  return {
    parentAxes: parentAxes.all.map((axis) => ({
      ...axis,
      url: parentAxisUrl(axis)
    })),

    projects: Object.values(projectAxisMappings.byId)
      .map((project) => ({
        ...project,
        childAxes: childAxes.all
          .filter((axis) => axis.project === project.id)
          .sort((first, second) => first.tag.localeCompare(second.tag))
          .map((axis) => ({
            ...axis,
          url: childAxisUrl(axis)
          }))
      }))
      .filter((project) => project.childAxes.length)
  };
}
