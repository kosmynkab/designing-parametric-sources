import parentAxes from "./parentAxes.js";
import projectAxisMappings from "./projectAxisMappings.js";
import projectChildAxes from "./projectChildAxes.js";

const parentAxisOrder = [
  "XOPQ",
  "YOPQ",
  "XTRA",
  "YTRA",
  "XTSP",
  "XSHA",
  "YSHA",
  "XSVA",
  "YSVA",
  "YTOS",
  "GRAD"
];

function parentAxisUrl(axis) {
  return `/reference/axes/${axis.id}/`;
}

function childAxisUrl(axis) {
  return `/reference/child-axes/${axis.tag.toLowerCase()}/`;
}

export default function referenceTree() {
  const childAxes = projectChildAxes();
  const projects = Object.values(projectAxisMappings.byId);

  function childAxesForParent(parentTag) {
    return projects.flatMap((project) =>
      (project.parentAxes[parentTag] || [])
        .map((tag) => childAxes.byProjectAndTag[project.id]?.[tag])
        .filter(Boolean)
        .map((axis) => ({
          ...axis,
          url: childAxisUrl(axis)
        }))
    );
  }

  return {
    parentAxes: parentAxes.all
      .map((axis) => ({
        ...axis,
        url: parentAxisUrl(axis),
        childAxes: childAxesForParent(axis.tag)
      }))
      .sort(
        (first, second) =>
          parentAxisOrder.indexOf(first.tag) - parentAxisOrder.indexOf(second.tag)
      ),

    otherAxes: ["BARS", "WDSP", "XTTW", "YTTL"].map((tag) => ({
      tag,
      url: `/reference/project-axes/${tag.toLowerCase()}/`
    }))
  };
}
