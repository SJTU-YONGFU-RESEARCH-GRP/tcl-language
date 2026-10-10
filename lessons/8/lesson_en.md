# Week 8 — Creating Geometry: cell, layer, polygon, wire, text + GDS

> Part of the [10-week Tcl learning plan](../../PLAN.md).  
> Goal this week: draw shapes with `$L create …` and export a GDS file.

**Environment:** Calibre DESIGNrev (same as Week 7). Run with `make week8-01` or `./scripts/run_calibre_tcl.sh`. Help: [docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md).

---

## Learning goals

By the end of this week, you should be able to:

1. Set units with `$L units microns 1000`.
2. Create a cell and layer (`create cell`, `create layer`).
3. Draw a rectangle/polygon with `$L create polygon`.
4. Add a text label with `$L create text`.
5. (Bonus) Draw a path with `$L create wire`.
6. Expand a coordinate list with `eval` when needed.
7. Write GDS with `$L gdsout` into `tmp/`.
8. Finish **my_shapes**: at least **polygon + text** (wire optional).

---

## Big idea

| API | Everyday metaphor | This week |
|-----|-------------------|-----------|
| `$L units microns` | Set the ruler scale | New blank layouts |
| `$L create cell` | Make a room | Usually `TOP` |
| `$L create layer` | Pick a colored sheet | `1` or `1.0` |
| `$L create polygon` | Connect dots into a shape | Boxes / rooms |
| `$L create wire` | Paint a road of width W | Paths |
| `$L create text` | Write a name on the map | Labels |
| `$L gdsout` | Save the drawing | File under `tmp/` |

Keep Week 7 OOP glasses: `$L create polygon ...` is still “object.method”.

---

## What you need before you start

### Prerequisites

- Week 7: `layout create`, handle `$L`, `create cell`, run via `run_calibre_tcl.sh`.

### Tools

```bash
make check-calibre
make week8-01
```

View GDS (parent helps): `./scripts/open_gds.sh tmp/week8_01_box.gds` if VNC is set up.

---

## Concept 1 — Units and room setup

```tcl
set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1
```

`units microns 1000` means: 1000 database units = 1 micron. New layouts often set this early.

See `02_units_microns.tcl`.

---

## Concept 2 — Layer number styles (important)

On **this** Calibre install:

| Style | `create layer` | `create polygon` |
|-------|----------------|------------------|
| `1` | OK | OK |
| `1.0` | OK | OK |
| `1_0` | **NOT** for create layer | OK for polygon after layer exists |

`examples/create_box.tcl` does: `create layer 1` then `create polygon TOP 1_0 ...`.

Pick one style per script and stay consistent. See `03_layer_styles.tcl`.

---

## Concept 3 — Polygon two ways

### Diagonal corners (manual Script 1)

```tcl
$L create polygon TOP 1 0 0 100 100
```

Two opposite corners → rectangle.

### Four corners (explicit)

```tcl
$L create polygon TOP 1_0 0 0 100 0 100 100 0 100
```

Same shape; every corner listed. See `04` and `05`.

---

## Concept 4 — Text and wire

```tcl
$L create text TOP 1 10 110 HELLO
$L create wire TOP 2_0 10 0 0 100 0 100 50
```

| Command | Meaning |
|---------|---------|
| `create text cell layer x y string` | Label at (x,y) |
| `create wire cell L_D width x1 y1 ...` | Path of given width |

See `06_create_text.tcl`, `07_create_wire.tcl`.

---

## Concept 5 — Coord list + `eval` (trap!)

`create polygon` wants **flat numbers**, not one nested list.

```tcl
set coords {0 0 40 0 40 30 0 30}
eval $L create polygon TOP 1 $coords
```

`eval` expands `$coords` into separate arguments. See `08_eval_coords_list.tcl` and `examples/script.tcl`.

---

## Concept 6 — Export GDS (and optional OASIS)

```tcl
$L gdsout tmp/week8_my_shapes.gds TOP
# optional:
$L oasisout tmp/week8.oas TOP
```

Always write under the project `tmp/` folder. See `11_oasisout_optional.tcl`.

---

## Daily practice

| Day | Goal | Files |
|-----|------|-------|
| Day 1 | Box like create_box | `01_create_box_like.tcl`, `02_units_microns.tcl` |
| Day 2 | Layer styles + sizes | `03_layer_styles.tcl`, `04`–`05` |
| Day 3 | Text label | `06_create_text.tcl` |
| Day 4 | Wire + eval | `07_create_wire.tcl`, `08_eval_coords_list.tcl` |
| Day 5 | **Project** | `10_my_shapes.tcl` |

### Week checklist

- [ ] units / cell / layer
- [ ] polygon (box)
- [ ] text
- [ ] wire (or try once)
- [ ] eval + coord list
- [ ] gdsout to `tmp/`
- [ ] finished `10_my_shapes.tcl`

---

## Common mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Unrecognized layernum... (1_0)` on create layer | `1_0` not valid for create layer here | Use `create layer 1` or `1.0` |
| Polygon fails if coords in one list | Nested list | `eval $L create polygon ... $coords` |
| `invalid command name "layout"` | Used tclsh | `make week8-NN` |
| No file in tmp | Wrong path | Use repo-root `tmp/` like examples |

---

## Example scripts

```bash
make week8-01
make week8
make list WEEK=8
```

| # | File | Practice |
|---|------|----------|
| 01 | `01_create_box_like.tcl` | Classic box → GDS |
| 02 | `02_units_microns.tcl` | units |
| 03 | `03_layer_styles.tcl` | 1 / 1.0 / 1_0 |
| 04 | `04_polygon_diagonal.tcl` | Two-corner rect |
| 05 | `05_polygon_four_corners.tcl` | Four corners |
| 06 | `06_create_text.tcl` | text |
| 07 | `07_create_wire.tcl` | wire |
| 08 | `08_eval_coords_list.tcl` | eval |
| 09 | `09_multi_shapes.tcl` | all three |
| 10 | `10_my_shapes.tcl` | **Week project** |
| 11 | `11_oasisout_optional.tcl` | OASIS bonus |
| 12 | `12_run_checklist.tcl` | Checklist |

---

## Challenge

Change `10_my_shapes.tcl`:

1. Your initials as text  
2. A different box size  
3. A wire that looks like a path through the box  
4. Print file size after `gdsout`  
5. (Optional) Also `oasisout`  

---

## Looking ahead

**Week 9** — query without redrawing: `layout peek`, `$L cells`, `$L layers`, `$L bbox`, `$L exists`. You will open the GDS you made this week and ask questions.

---

## Parent / teacher note

- Layer style quirks are environment-specific; this machine prefers `create layer 1` then polygon `1` / `1.0` / `1_0`.
- GUI open is optional for verification.
- Success: child runs `make week8-10`, sees a GDS under `tmp/`, can name polygon vs text.
