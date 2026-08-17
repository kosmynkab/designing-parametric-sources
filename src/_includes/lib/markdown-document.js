import matter from "gray-matter";
import MarkdownIt from "markdown-it";

const markdown = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: false
});

function slugify(value) {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^\p{L}\p{N}]+/gu, "-")
    .replace(/^-+|-+$/g, "");
}

function sourceSlice(lines, start, end) {
  return lines.slice(start, end).join("\n").trim();
}

function findSections(tokens, lines) {
  const headings = [];

  for (let index = 0; index < tokens.length; index += 1) {
    const token = tokens[index];

    if (
      token.type !== "heading_open" ||
      token.tag !== "h2" ||
      !token.map
    ) {
      continue;
    }

    const inlineToken = tokens[index + 1];

    headings.push({
      title: inlineToken.content,
      id: slugify(inlineToken.content),
      start: token.map[0],
      contentStart: token.map[1]
    });
  }

  const sections = {};

  for (let index = 0; index < headings.length; index += 1) {
    const heading = headings[index];
    const nextHeading = headings[index + 1];
    const end = nextHeading ? nextHeading.start : lines.length;
    const source = sourceSlice(lines, heading.contentStart, end);

    if (sections[heading.id]) {
      throw new Error(`Duplicate section id "${heading.id}"`);
    }

    sections[heading.id] = {
      id: heading.id,
      title: heading.title,
      source,
      html: markdown.render(source)
    };
  }

  return {
    headings,
    sections
  };
}

function findNotes(tokens, lines) {
  const notes = [];
  const seenRanges = new Set();

  for (const token of tokens) {
    if (token.type !== "blockquote_open" || !token.map) {
      continue;
    }

    const [start, end] = token.map;
    const range = `${start}:${end}`;

    if (seenRanges.has(range)) {
      continue;
    }

    seenRanges.add(range);

    const source = sourceSlice(lines, start, end);

    notes.push({
      source,
      html: markdown.render(source)
    });
  }

  return notes;
}

export function parseMarkdownDocument(source, filePath = "Markdown document") {
  const { data, content } = matter(source);
  const lines = content.split(/\r?\n/);
  const tokens = markdown.parse(content, {});
  const { headings, sections } = findSections(tokens, lines);
  const firstHeading = headings[0];

  const preambleSource = firstHeading
    ? sourceSlice(lines, 0, firstHeading.start)
    : content.trim();

  const orderedSections = headings.map((heading) => sections[heading.id]);

  return {
    ...data,
    source: content.trim(),
    html: markdown.render(content),
    preamble: {
      source: preambleSource,
      html: markdown.render(preambleSource)
    },
    sections,
    notes: findNotes(tokens, lines),
    blocks: [
      ...(preambleSource
        ? [
            {
              type: "preamble",
              source: preambleSource,
              html: markdown.render(preambleSource)
            }
          ]
        : []),
      ...orderedSections.map((section) => ({
        type: "section",
        ...section
      }))
    ]
  };
}