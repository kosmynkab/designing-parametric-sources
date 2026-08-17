# Parametric Sources Worklist

Status: `[x]` working structure · `[-]` draft content · `[ ]` not started.

## Immediate sequence

- [-] **XOPQ → XOUC** — refine the canonical argument and XOUC commentary.
- [-] **YOPQ → YOUC** — refine the canonical argument and YOUC commentary.
- [ ] **XTRA → XTUC** — next vertical slice.
- [ ] **YTRA → YTUC** — next vertical slice.
- [ ] Return to the remaining XOPQ and YOPQ implementation axes.

## Canonical-axis pages

Each canonical axis has a Markdown source and a page template.

| Status | Axis | Markdown | Page |
| --- | --- | --- | --- |
| [-] | XOPQ | `src/_data/canonical-axes/xopq.md` | `src/reference/axes/XOPQ/index.njk` |
| [-] | YOPQ | `src/_data/canonical-axes/yopq.md` | `src/reference/axes/YOPQ/index.njk` |
| [ ] | XTRA | `src/_data/canonical-axes/xtra.md` | `src/reference/axes/XTRA/index.njk` |
| [ ] | YTRA | `src/_data/canonical-axes/ytra.md` | `src/reference/axes/YTRA/index.njk` |
| [ ] | XTSP | `src/_data/canonical-axes/xtsp.md` | `src/reference/axes/XTSP/index.njk` |
| [ ] | XSHA | `src/_data/canonical-axes/xsha.md` | `src/reference/axes/XSHA/index.njk` |
| [ ] | YSHA | `src/_data/canonical-axes/ysha.md` | `src/reference/axes/YSHA/index.njk` |
| [ ] | XSVA | `src/_data/canonical-axes/xsva.md` | `src/reference/axes/XSVA/index.njk` |
| [ ] | YSVA | `src/_data/canonical-axes/ysva.md` | `src/reference/axes/YSVA/index.njk` |
| [ ] | XTEQ | `src/_data/canonical-axes/xteq.md` | `src/reference/axes/XTEQ/index.njk` |
| [ ] | YTEQ | `src/_data/canonical-axes/yteq.md` | `src/reference/axes/YTEQ/index.njk` |
| [ ] | YTOS | `src/_data/canonical-axes/ytos.md` | `src/reference/axes/YTOS/index.njk` |
| [ ] | GRAD | `src/_data/canonical-axes/grad.md` | `src/reference/axes/GRAD/index.njk` |

## Amstelvar Avar2 design-axis pages

For every design-axis tag below, create these two files:

```text
src/_data/projects/amstelvar-a2/design-axes/<tag-lowercase>.md
src/reference/design-axes/<TAG-UPPERCASE>/index.njk
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

- [ ] `src/_data/canonical-axes.json` maps `XVAA → XVAU`, but no XVAA canonical Markdown/page exists. Decide whether to add it or remove the mapping.

## Reusable page tools

- Canonical-page renderer: `src/_includes/canonical-axis-document.njk`
- Project design-axis renderer: `src/_includes/project-design-axis-document.njk`
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
