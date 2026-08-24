# Parametric Sources Worklist

Status: `[x]` working structure · `[-]` draft content · `[ ]` not started.

## Immediate sequence

- [-] **XOPQ → XOUC** — refine the parent argument and XOUC commentary.
- [-] **YOPQ → YOUC** — refine the parent argument and YOUC commentary.
- [ ] **XTRA → XTUC** — next vertical slice.
- [ ] **YTRA → YTUC** — next vertical slice.
- [ ] Return to the remaining XOPQ and YOPQ implementation axes.

## Parent-axis pages

Each parent axis has a Markdown source and a page template.

| Status | Axis | Markdown | Page |
| --- | --- | --- | --- |
| [-] | XOPQ | `src/_data/parent-axes/xopq.md` | `src/reference/axes/XOPQ/index.njk` |
| [-] | YOPQ | `src/_data/parent-axes/yopq.md` | `src/reference/axes/YOPQ/index.njk` |
| [-] | XTRA | `src/_data/parent-axes/xtra.md` | `src/reference/axes/XTRA/index.njk` |
| [-] | YTRA | `src/_data/parent-axes/ytra.md` | `src/reference/axes/YTRA/index.njk` |
| [-] | XTSP | `src/_data/parent-axes/xtsp.md` | `src/reference/axes/XTSP/index.njk` |
| [-] | XSHA | `src/_data/parent-axes/xsha.md` | `src/reference/axes/XSHA/index.njk` |
| [-] | YSHA | `src/_data/parent-axes/ysha.md` | `src/reference/axes/YSHA/index.njk` |
| [-] | XSVA | `src/_data/parent-axes/xsva.md` | `src/reference/axes/XSVA/index.njk` |
| [-] | YSVA | `src/_data/parent-axes/ysva.md` | `src/reference/axes/YSVA/index.njk` |
| [-] | XTEQ | `src/_data/parent-axes/xteq.md` | `src/reference/axes/XTEQ/index.njk` |
| [-] | YTEQ | `src/_data/parent-axes/yteq.md` | `src/reference/axes/YTEQ/index.njk` |
| [-] | YTOS | `src/_data/parent-axes/ytos.md` | `src/reference/axes/YTOS/index.njk` |
| [-] | GRAD | `src/_data/parent-axes/grad.md` | `src/reference/axes/GRAD/index.njk` |

## Amstelvar Avar2 child-axis pages

For every child-axis tag below, create these two files:

```text
src/_data/projects/amstelvar-a2/child-axes/<tag-lowercase>.md
src/reference/project-implementation/<TAG-UPPERCASE>/index.njk
```

### XOPQ — thick strokes

- [-] XOUC
- [ ] XOLC
- [ ] XOFI
- [ ] XOET
- [ ] XOUA
- [ ] XOLA

### YOPQ — thin strokes

- [-] YOUC
- [ ] YOLC
- [ ] YOFI
- [ ] YOET
- [ ] YOUA
- [ ] YOLA

### XTRA — horizontal transparency

- [ ] XTUC, XTUR, XTUD, XTUA
- [ ] XTLC, XTLR, XTLD, XTLA
- [ ] XTFI, XTET

### YTRA — vertical transparency

- [ ] YTUC, YTLC, YTFI, YTAS, YTDE

### XTSP — side spacing

- [ ] XUCS, XUCD, XUCR
- [ ] XLCS, XLCD, XLCR
- [ ] XFIR, XETS

### Serif transformations

- [ ] XSHA: XSHU, XSHL, XSHF
- [ ] YSHA: YSHU, YSHL, YSHF
- [ ] XSVA: XSVU, XSVL, XSVF
- [ ] YSVA: YSVU, YSVL, YSVF

### Equalisation, overshoot, and grade

- [ ] XTEQ: XQUC, XQLC, XQFI
- [ ] YTEQ: YQUC, YQLC, YQFI
- [ ] YTOS: YTOS
- [ ] GRAD: GRAD

## Open structural question

- [ ] `src/_data/parent-axes.json` maps `XVAA → XVAU`, but no XVAA parent Markdown/page exists. Decide whether to add it or remove the mapping.

## Reusable page tools

- Parent-page renderer: `src/_includes/parent-axis-document.njk`
- Project child-axis renderer: `src/_includes/project-child-axis-document.njk`
- Automatic min/max specimen pair: `src/_includes/project-axis-specimen-pair.njk`

### Specimen-pair callout

```njk
{% set specimenProject = "amstelvar-a2" %}
{% set specimenAxis = "XOUC" %}
{% set specimenGlyph = "H" %}
{% set specimenStyle = "roman" %}
{% include "project-axis-specimen-pair.njk" %}
```

Only change `specimenAxis`, `specimenGlyph`, and `specimenStyle` to select a different pair.
