import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseMarkdownDocument } from "../_includes/lib/markdown-document.js";

const dataDirectory = path.dirname(fileURLToPath(import.meta.url));
const projectsDirectory = path.join(dataDirectory, "projects");

function readDesignAxis(projectId, fileName) {
  const filePath = path.join(
    projectsDirectory,
    projectId,
    "design-axes",
    fileName
  );

  const axis = parseMarkdownDocument(
    fs.readFileSync(filePath, "utf8"),
    filePath
  );

  const fileId = path.basename(fileName, ".md");

  for (const field of ["id", "tag", "project", "canonicalAxis", "scope", "summary"]) {
    if (!axis[field]) {
      throw new Error(`Missing "${field}" in ${filePath}`);
    }
  }

  if (axis.id !== fileId) {
    throw new Error(
      `Axis id "${axis.id}" does not match file name "${fileName}"`
    );
  }

  if (axis.project !== projectId) {
    throw new Error(
      `Project "${axis.project}" does not match directory "${projectId}"`
    );
  }

  return axis;
}

export default function projectDesignAxes() {
  const all = fs
    .readdirSync(projectsDirectory, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .flatMap((project) => {
      const designAxesDirectory = path.join(
        projectsDirectory,
        project.name,
        "design-axes"
      );

      if (!fs.existsSync(designAxesDirectory)) {
        return [];
      }

      return fs
        .readdirSync(designAxesDirectory)
        .filter((fileName) => fileName.endsWith(".md"))
        .map((fileName) => readDesignAxis(project.name, fileName));
    });

  const byProjectAndTag = {};

  for (const axis of all) {
    byProjectAndTag[axis.project] ||= {};
    byProjectAndTag[axis.project][axis.id] = axis;
  }

  return {
    all,
    byProjectAndTag
  };
}