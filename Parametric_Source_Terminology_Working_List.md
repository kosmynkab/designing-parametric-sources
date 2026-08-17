# Parametric Fonts and Source Design – Working Vocabulary

This is a working list for the archive’s future dictionary and reference material. It assumes an advanced type-design reader, so it does not attempt to define general typographic concepts unless their use in parametric source design needs clarification.

The planned first step is a simple Explanation landing page. The dictionary can become one of its sub-pages once the core definitions have been written and reviewed.

## 1. Core dictionary

### Parametric-source concepts

- Parametric design
- Parametric font
- Parametric typeface
- Parametric axis
- Parametric source
- Parametric source system
- Canonical axis
- Canonical transformation
- Design axis
- Project-specific design axis
- Design-axis mapping
- Axis decomposition
- Axis variation
- Axis interaction
- Compensation
- Semantic space
- Design space
- Style range
- Blend
- Blended state
- Neutral state
- Source extreme
- Instance
- Master
- Delta

### Research and archive concepts

- Evidence
- Specimen
- Proofing specimen
- Evidence catalogue
- Research block
- Construction case
- Control construction
- Supporting construction
- Outlier
- Observation
- Intentional comparison
- Exception
- Open question
- Reproducible evidence
- Source data

## 2. Contextual design terms

Add a definition only when the term has a specific role in the parametric-source system or in the archive’s research method.

- Counter adjustment
- White channel
- Ascending/descender length
- Vertical metrics
- Line metrics
- Optical sizing automation
- Dark-mode compensation
- Justification
- Multi-script support
- Script coverage
- CJK
- Style range limitation

## 3. Technical reference vocabulary

These terms belong in a technical reference or appendix rather than the core conceptual dictionary.

- Variable font
- Variable-font technology
- `AVAR2` / Axis Variations v2
- `fvar`
- `STAT`
- `hhea`
- `OS/2`
- `GSUB`
- Designspace
- Hinting
- Optical sizing
- File-size optimisation
- Font compression
- Interpolation efficiency
- Rendering size

> Keep **design space** (the conceptual or interpolation space) distinct from **Designspace** (the source-format/document term).

## 4. Canonical-axis register

Canonical axes should form a structured reference rather than ordinary glossary entries. Each record can later include its transformation statement, relevant project-specific design axes, selected evidence, and exceptions.

- `XOPQ`
- `YOPQ`
- `XTRA`
- `YTRA`
- `XTSP`
- `XSHA`
- `YSHA`
- `XSVA`
- `YSVA`
- `GRAD`
- `XTEQ`
- `YTEQ`
- `YTOS`

Terms such as weight axis, width axis, optical-size axis, and grade axis may be useful points of comparison, but should not be assumed to be equivalent to the archive’s canonical axes.

## 5. Amstelvar Avar2 design-axis register

Amstelvar Avar2 design-axis identifiers are project data, not universal terminology. Each entry should record:

- Identifier
- Parent canonical axis
- Glyph or construction scope
- Source or data location
- Relationships to other Amstelvar design axes

Known examples:

- `XOUC`
- `XOLC`
- `XOFI`
- `XOET`

The complete list should be drawn from the project’s source mapping.

## Editorial notes

- Define generic concepts first, then use Amstelvar Avar2 as an example.
- Keep common type-design vocabulary in ordinary prose unless the archive gives it a specialised meaning.
- Preserve the distinction between canonical axes, project-specific design axes, and technical variable-font implementation.
- Use British spelling in reader-facing definitions.
