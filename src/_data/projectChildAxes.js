import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseMarkdownDocument } from "../_includes/lib/markdown-document.js";

const dataDirectory = path.dirname(fileURLToPath(import.meta.url));
const projectsDirectory = path.join(dataDirectory, "projects");

function readChildAxis(projectId, fileName) {
  const filePath = path.join(
    projectsDirectory,
    projectId,
    "child-axes",
    fileName
  );

  const axis = parseMarkdownDocument(
    fs.readFileSync(filePath, "utf8"),
    filePath
  );

  const fileSlug = path.basename(fileName, ".md");

  for (const field of ["tag", "project", "parentAxis", "scope", "summary"]) {
    if (!axis[field]) {
      throw new Error(`Missing "${field}" in ${filePath}`);
    }
  }

  if (axis.tag.toLowerCase() !== fileSlug) {
    throw new Error(
      `Child axis tag "${axis.tag}" does not match file name "${fileName}"`
    );
  }

  if (axis.project !== projectId) {
    throw new Error(
      `Project "${axis.project}" does not match directory "${projectId}"`
    );
  }

  return axis;
}

export default function projectChildAxes() {
  const all = fs
    .readdirSync(projectsDirectory, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .flatMap((project) => {
      const childAxesDirectory = path.join(
        projectsDirectory,
        project.name,
        "child-axes"
      );

      if (!fs.existsSync(childAxesDirectory)) {
        return [];
      }

      return fs
        .readdirSync(childAxesDirectory)
        .filter((fileName) => fileName.endsWith(".md"))
        .map((fileName) => readChildAxis(project.name, fileName));
    });

  const byProjectAndTag = {};

  for (const axis of all) {
    byProjectAndTag[axis.project] ||= {};
    byProjectAndTag[axis.project][axis.tag] = axis;
  }

  return {
    all,
    byProjectAndTag
  };
}
