XOPQ
====

Expected behavior: thick strokes get thinner/thicker while everything else “stays the same”.


Uppercase
---------

### Straight glyphs

- only XOPQ changes
- only x-direction deltas
- control glyph `H`

##### XOPQ max

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Roman_H_XOUCmax.svg)

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Italic_H_XOUCmax.svg)

##### XOPQ min

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Roman_H_XOUCmin.svg)

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Italic_H_XOUCmin.svg)


### Round glyphs

- only x-direction deltas (?),
- control glyph `O`

> In AmstelvarA2 Italic, should we add some rotation with y-deltas? See [XTRA / Round glyphs](../XTRA/#round-glyphs).

##### XOPQ max

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Roman_O_XOUCmax.svg)

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Italic_O_XOUCmax.svg)

##### XOPQ min

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Roman_O_XOUCmin.svg)

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Italic_O_XOUCmin.svg)


### Diagonal glyphs

- control glyph `V`
- angle of slanted strokes does not change
- xy-direction deltas allowed in slanted strokes
- in AmstelvarA2, slanted measurements are aligned to stroke
- XTRA may change slightly to accommodate angles

> In RobotoDelta, the angle of slanted strokes is different from the default.

##### XOPQ max

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Roman_V_XOUCmax.svg)

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Italic_V_XOUCmax.svg)

##### XOPQ min

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Roman_V_XOUCmin.svg)

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Italic_V_XOUCmin.svg)

> The italic V in XOPQmin seems like its too thick.

### Single-stem glyphs

- XTRA should increase proportionally with XOPQ, to account for second vertical stroke in control glyph

##### XOPQ max

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Roman_E_XOUCmax.svg)

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Italic_E_XOUCmax.svg)

##### XOPQ min

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Roman_E_XOUCmin.svg)

![](src/imgs-svg/amstelvar-a2/uc/AmstelvarA2-Italic_E_XOUCmin.svg)

> Is the italic E not too narrow in XOPQmin?

Lowercase
---------

### Straight glyphs

AmstelvarA2 Roman:

- Mostly x-direction deltas and a little bit of y-direction deltas in XOLC max
- YOLC changes on XOLC max because of /n's shoulder translation
- Only x-direction delta in XOLC min (?)

##### XOPQ max

![](src/imgs-svg/amstelvar-a2/lc/AmstelvarA2-Roman_n_XOLCmax.svg)

![](src/imgs-svg/amstelvar-a2/lc/AmstelvarA2-Italic_n_XOLCmax.svg)

##### XOPQ min

![](src/imgs-svg/amstelvar-a2/lc/AmstelvarA2-Roman_n_XOLCmin.svg)

![](src/imgs-svg/amstelvar-a2/lc/AmstelvarA2-Italic_n_XOLCmin.svg)

### Round glyphs

AmstelvarA2 Roman:

- only x-direction deltas

##### XOPQ max

![](src/imgs-svg/amstelvar-a2/lc/AmstelvarA2-Roman_o_XOLCmax.svg)

![](src/imgs-svg/amstelvar-a2/lc/AmstelvarA2-Italic_o_XOLCmax.svg)

##### XOPQ min

![](src/imgs-svg/amstelvar-a2/lc/AmstelvarA2-Roman_o_XOLCmin.svg)

![](src/imgs-svg/amstelvar-a2/lc/AmstelvarA2-Italic_o_XOLCmin.svg)

### Diagonal glyphs

AmstelvarA2 Roman:

- angle of slanted strokes does not change
- xy-direction deltas allowed in slanted strokes
- slanted measurements are aligned to stroke
- XTRA may change slightly to accommodate angles

##### XOPQ max

![](src/imgs-svg/amstelvar-a2/lc/AmstelvarA2-Roman_v_XOLCmax.svg)

![](src/imgs-svg/amstelvar-a2/lc/AmstelvarA2-Italic_v_XOLCmax.svg)

##### XOPQ min

![](src/imgs-svg/amstelvar-a2/lc/AmstelvarA2-Roman_v_XOLCmin.svg)

![](src/imgs-svg/amstelvar-a2/lc/AmstelvarA2-Italic_v_XOLCmin.svg)


Figures
-------

### Straight glyphs

AmstelvarA2 Roman:

- XOFI changes
- Since it's a single stem glyph XTRA changes according to the XOPQ

##### XOPQ max

![](src/imgs-svg/amstelvar-a2/other/AmstelvarA2-Roman_one_XOFImax.svg)

![](src/imgs-svg/amstelvar-a2/other/AmstelvarA2-Italic_one_XOFImax.svg)

##### XOPQ min

![](src/imgs-svg/amstelvar-a2/other/AmstelvarA2-Roman_one_XOFImin.svg)

![](src/imgs-svg/amstelvar-a2/other/AmstelvarA2-Italic_one_XOFImin.svg)

### Round glyphs

AmstelvarA2 Roman:

- only x-direction deltas

##### XOPQ max

![](src/imgs-svg/amstelvar-a2/other/AmstelvarA2-Roman_zero_XOFImax.svg)

![](src/imgs-svg/amstelvar-a2/other/AmstelvarA2-Italic_zero_XOFImax.svg)

##### XOPQ min

![](src/imgs-svg/amstelvar-a2/other/AmstelvarA2-Roman_zero_XOFImin.svg)

![](src/imgs-svg/amstelvar-a2/other/AmstelvarA2-Italic_zero_XOFImin.svg)


Etcetera
--------

### Accents

#### XOPQ min

#### XOPQ max


### Symbols

#### XOPQ min

#### XOPQ max


Greek
--------



Cyrillic
--------
