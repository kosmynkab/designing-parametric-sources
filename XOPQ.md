XOPQ
====

Expected behavior: thick strokes get thicker while everything else “stays the same”.


Uppercase
---------

### Straight glyphs

- only XOPQ changes
- only x-direction deltas

##### XOPQ max

![](imgs/AmstelvarA2-Roman_H__XOPQmax.png)

![](imgs/AmstelvarA2-Italic_H__XOPQmax.png)

##### XOPQ min

![](imgs/AmstelvarA2-Roman_H__XOPQmin.png)

![](imgs/AmstelvarA2-Italic_H__XOPQmin.png)

### Round glyphs

- only x-direction deltas (?)

> In AmstelvarA2 Italic, should we add some rotation with y-deltas? See [XTRA / Round glyphs](../XTRA/#round-glyphs).

##### XOPQ max

![](imgs/AmstelvarA2-Roman_O__XOPQmax.png)

##### XOPQ min

![](imgs/AmstelvarA2-Roman_O__XOPQmin.png)


### Diagonal glyphs

- angle of slanted strokes does not change
- xy-direction deltas allowed in slanted strokes
- in AmstelvarA2, slanted measurements are aligned to stroke
- XTRA may change slightly to accommodate angles

> In RobotoDelta, the angle of slanted strokes is different from the default.

##### XOPQ max

/V

##### XOPQ min

/V

### Single-stem glyphs

- XTRA should increase proportionally with XOPQ, to account for second vertical stroke in control glyph

##### XOPQ max

/E

##### XOPQ min

/E


Lowercase
---------

### Straight glyphs

AmstelvarA2 Roman:

- Mostly x-direction deltas and a little bit of y-direction deltas in XOLC max
- YOLC changes on XOLC max because of /n's shoulder translation
- Only x-direction delta in XOLC min (?)

##### XOPQ max

![](imgs/AmstelvarA2-Roman_n_XOPQmax.png)

##### XOPQ min

![](imgs/AmstelvarA2-Roman_n_XOPQmin.png)

### Round glyphs

AmstelvarA2 Roman:

- only x-direction deltas

##### XOPQ max

/o

##### XOPQ min

/o

### Diagonal glyphs

AmstelvarA2 Roman:

- angle of slanted strokes does not change
- xy-direction deltas allowed in slanted strokes
- slanted measurements are aligned to stroke
- XTRA may change slightly to accommodate angles

##### XOPQ max

/v

##### XOPQ min

/v


Figures
-------

### Straight glyphs

AmstelvarA2 Roman:

- XOFI changes
- Since it's a single stem glyph XTRA changes according to the XOPQ

##### XOPQ max

/one

##### XOPQ min

/one

### Round glyphs

AmstelvarA2 Roman:

- only x-direction deltas

##### XOPQ max

/zero

##### XOPQ min

/zero


Etcetera
--------

...

