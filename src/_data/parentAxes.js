import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseMarkdownDocument } from "../_includes/lib/markdown-document.js";

const dataDirectory = path.dirname(fileURLToPath(import.meta.url));
const parentAxesDirectory = path.join(dataDirectory, "parent-axes");

function readParentAxis(fileName) {
  const filePath = path.join(parentAxesDirectory, fileName);
  const source = fs.readFileSync(filePath, "utf8");
  const axis = parseMarkdownDocument(source, filePath);
  const fileId = path.basename(fileName, ".md");

  for (const field of ["id", "tag", "title", "summary"]) {
    if (!axis[field]) {
      throw new Error(`Missing "${field}" in ${filePath}`);
    }
  }

  if (axis.id !== fileId) {
    throw new Error(
      `Axis id "${axis.id}" does not match file name "${fileName}"`
    );
  }

  return {
    ...axis,
    fileName
  };
}

const all = fs
  .readdirSync(parentAxesDirectory)
  .filter((fileName) => fileName.endsWith(".md"))
  .sort()
  .map(readParentAxis)
  .sort((first, second) => first.tag.localeCompare(second.tag));

const byId = Object.fromEntries(
  all.map((axis) => [axis.id, axis])
);

export default {
  all,
  byId
};