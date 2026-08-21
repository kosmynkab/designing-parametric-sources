import fs from "node:fs";

const researchFiles = {
  xopq: ["1_XOPQ.md", "XOPQ"],
  yopq: ["2_YOPQ.md", "YOPQ"],
  xtra: ["3_XTRA.md", "XTRA"],
  ytra: ["4_YTRA.md", "YTRA"],
  xtsp: ["5_XTSP.md", "XTSP"],
  xsha: ["6_XSHA.md", "XSHA"],
  ysha: ["7_YSHA.md", "YSHA"],
  xsva: ["8_XSVA.md", "XSVA"],
  ysva: ["9_YSVA.md", "YSVA"],
  grad: ["D_GRAD.md", "GRAD"]
};

const groupLabels = {
  uppercase: "Uppercase",
  lowercase: "Lowercase",
  figures: "Figures",
  punctuation: "Punctuation",
  symbols: "Symbols",
  parts: "Parts"
};

const specimens = JSON.parse(
  fs.readFileSync(new URL("./specimens.json", import.meta.url), "utf8")
).specimens;

function selectedSpecimens(researchFile, parentAxis) {
  const markdown = fs.readFileSync(
    new URL(`../../${researchFile}`, import.meta.url),
    "utf8"
  );
  const references = [
    ...markdown.matchAll(
      /AmstelvarA2-(Roman|Italic)_([^_]+)_[A-Z]+(min|max)\.png/g
    )
  ];
  const groups = [];

  for (const reference of references) {
    const [, style, glyph, instance] = reference;
    const specimen = specimens.find(
      (item) =>
        item.parent_axis === parentAxis &&
        item.style === style.toLowerCase() &&
        item.glyph === glyph &&
        item.instance === instance
    );

    // Some source notes reference combinations that have not been exported.
    if (!specimen) continue;

    let group = groups.find((item) => item.id === specimen.group);
    if (!group) {
      group = {
        id: specimen.group,
        label: groupLabels[specimen.group] || specimen.group,
        specimens: []
      };
      groups.push(group);
    }

    group.specimens.push(specimen);
  }

  return { groups };
}

export default Object.fromEntries(
  Object.entries(researchFiles).map(([id, [file, parentAxis]]) => [
    id,
    selectedSpecimens(file, parentAxis)
  ])
);
