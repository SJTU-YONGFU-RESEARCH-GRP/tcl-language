# Week 28 — Shape Booleans: `$L AND` / `OR` / `NOT` / `SIZE`

> Optional advanced week after the [10-week plan](../../PLAN.md).  
> Goal: overlap, merge, subtract layers — and grow/shrink outlines.

**Environment:** Calibre DESIGNrev. Help: [docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md).

---

## Learning goals

1. Build two overlapping polygons on layers 1 and 2.
2. Run `$L AND 1 2 3` and inspect the result with `iterator poly`.
3. Do the same for `OR` and `NOT`.
4. Grow/shrink with `$L SIZE 1 3 by 0.001` / `by -0.001` (with `units microns 1000`).
5. Finish **boolean_poster**: `tmp/week28_poster.gds` + report.

---

## Big idea

| Op | Everyday | Result |
|----|----------|--------|
| AND | Two stickers’ overlap | Only the shared region |
| OR | Glue both stickers | One big outline |
| NOT | Cut sticker B out of A | A with a bite taken |
| SIZE | Inflate / shrink a balloon | Fatter or thinner outline |
| XOR | Only exclusive parts | Both stickers minus overlap |

---

## Prerequisites

- Week 8: layers + polygons
- Week 11: `iterator poly` to check results
- Calibre via `./scripts/run_calibre_tcl.sh`

---

## Concept 1 — Overlapping inputs

```tcl
$L create polygon TOP 1_0 0 0 20 20
$L create polygon TOP 2_0 10 10 30 30
# overlap ≈ (10,10)-(20,20)
```

See `01_build_overlap.tcl`.

---

## Concept 2 — AND / OR / NOT / XOR

```tcl
$L AND 1 2 3          ;# intersection → layer 3
$L OR  1 2 4          ;# union         → layer 4
$L NOT 1 2 5          ;# L1 minus L2   → layer 5
$L XOR 1 2 6          ;# exclusive-or  → layer 6
```

Usage shape (AND/NOT/XOR):

```
$L AND <in1> <in2> <out> [-cell <cell> [-hier 0|1]]
```

Layers are numbers (`1 2 3`), not `1_0`. Output layer should already exist (`create layer`).

See `03_and.tcl` … `06_xor.tcl`, `11_compare_all.tcl`.

---

## Concept 3 — SIZE grow / shrink

```tcl
$L units microns 1000
$L SIZE 1 3 by 0.001    ;# ~+1 µm on the drawing
$L SIZE 1 3 by -0.001   ;# ~−1 µm (shrink)
```

Form that works here: `$L SIZE <in> <out> by <amount>`.

**Caution:** large amounts (like `by 1`) explode the geometry. Start with `0.001`.

See `07_size_grow.tcl`, `08_size_shrink.tcl`.

---

## Concept 4 — `-cell`

```tcl
$L AND 1 2 3 -cell TOP
```

Limits the boolean to one cell. See `09_and_cell.tcl`.

---

## Daily practice

| Day | Goal | Files |
|-----|------|-------|
| 1 | Overlap + AND | `01`, `02`, `03` |
| 2 | OR + NOT | `04`, `05` |
| 3 | SIZE grow/shrink | `07`, `08` |
| 4 | XOR + `-cell` | `06`, `09`, `11` |
| 5 | **boolean_poster** | `10` |

### Checklist

- [ ] AND overlap  
- [ ] OR / NOT  
- [ ] SIZE ±0.001  
- [ ] Optional XOR / `-cell`  
- [ ] Poster GDS + report  

---

## Common mistakes

| Symptom | Fix |
|---------|-----|
| `Expected <inlayer1>…` | Order is `in1 in2 out` — no cell name in front |
| Empty SIZE result / huge box | Use `by 0.001`, not `by 1` |
| No polys on out layer | `create layer` for the output first |
| Wrong cell unchanged | Add `-cell TOP` if you only want one cell |

---

## Example scripts

```bash
make week28-01
make week28
make week28-10
```

| # | File | Focus |
|---|------|-------|
| 01 | `01_build_overlap.tcl` | Inputs |
| 02 | `02_boolean_usage.tcl` | Usage |
| 03 | `03_and.tcl` | AND |
| 04 | `04_or.tcl` | OR |
| 05 | `05_not.tcl` | NOT |
| 06 | `06_xor.tcl` | XOR |
| 07 | `07_size_grow.tcl` | SIZE grow |
| 08 | `08_size_shrink.tcl` | SIZE shrink |
| 09 | `09_and_cell.tcl` | `-cell` |
| 10 | `10_boolean_poster.tcl` | **project** |
| 11 | `11_compare_all.tcl` | Counts table |
| 12 | `12_run_checklist.tcl` | Checklist |

---

## Challenge

Draw a ring: big OR of two boxes, then NOT out a smaller inner box (use a third input layer), write the ring to layer 8.

---

## Looking ahead

Next: [Week 15 — `string` family](../15/lesson_en.md) (Catalog A). Full map: [docs/COVERAGE.md](../../docs/COVERAGE.md).

---

## Parent / teacher note

Optional week. Success: `make week28-10` writes `tmp/week28_poster.gds` and `tmp/week28_report.txt`. Uses calibredrv.
