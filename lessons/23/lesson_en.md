# Week 23 — Query and Inspect: open, ask, peek

> Part of the [10-week Tcl learning plan](../../PLAN.md).  
> Goal this week: open a GDS, ask questions with query APIs, and use `layout peek` without redrawing.

**Environment:** Calibre DESIGNrev. Prefer GDS from Week 8 (`tmp/week8_my_shapes.gds`). Help: [docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md).

---

## Learning goals

By the end of this week, you should be able to:

1. Use `layout peek $gds -cells/-layers/-topcell` for a fast look.
2. Open a file with `set L [layout create $gds]` (optionally `-dt_expand`).
3. Print `$L topcell`, `$L cells`, `$L layers`.
4. Use `$L exists cell` / `$L exists layer` with friendly `if` messages.
5. Print `$L bbox cellName` (how big the cell is).
6. Explain **peek vs full create** in one sentence.
7. Finish **report_gds**: a script that prints a full report (optional path argument).

When you can report on your own Week 8 GDS using ≥4 query APIs, Week 23 is done.

---

## Big idea

Week 8 = **draw**. Week 23 = **ask**.

| API | Everyday metaphor | This week |
|-----|-------------------|-----------|
| `layout peek` | Look through the window (don’t open the whole house) | Fast cells/layers/top |
| `layout create $gds` | Open the house and get a key (`$L`) | Full load |
| `$L topcell` | What is the main room called? | Name |
| `$L cells` / `$L layers` | List rooms / colored sheets | Inventory |
| `$L exists …` | Is there a room named TOP? | Yes/no |
| `$L bbox` | How big is that room? | Bounding box |
| `$L file` | Which file did this come from? | Source path |

You do **not** need to create polygons this week. Use last week’s GDS.

---

## What you need before you start

### Prerequisites

- Week 7–8: handles, `gdsout`, run via calibredrv.

### Prepare a sample GDS

```bash
make week8-10          # creates tmp/week8_my_shapes.gds
make week23-01          # confirms a sample file exists
```

---

## Concept 1 — `layout peek` (fast look)

```tcl
puts [layout peek $gds -cells]
puts [layout peek $gds -layers]
puts [layout peek $gds -topcell]
puts [layout peek $gds -precision]
puts [layout peek $gds -units]
```

Peek does **not** give you a long-lived handle for `$L bbox` etc. It answers quick questions.

See `02_peek_cells_layers.tcl`, `03_peek_precision_units.tcl`.

---

## Concept 2 — Full open: `layout create $gds`

```tcl
set L [layout create $gds]
# or keep datatype detail:
set L [layout create $gds -dt_expand]
puts "Handle = $L"
```

Same pattern as Week 7 empty create — but the paper already has drawings.

See `04_open_gds_handle.tcl`.

---

## Concept 3 — Ask `$L` questions

```tcl
puts [$L topcell]
puts [$L cells]
puts [$L layers]
puts [$L file]
```

See `05_topcell_cells_layers.tcl`, `08_exists_layer_and_file.tcl`.

---

## Concept 4 — `exists` and `bbox`

```tcl
if {[$L exists cell TOP]} {
    puts "bbox TOP = [$L bbox TOP]"
} else {
    puts "no cell TOP"
}
```

`bbox` returns something like `0 0 120 90` (left bottom right top).

See `06_exists_cell.tcl`, `07_bbox_cell.tcl`.

---

## Concept 5 — Peek vs create (Day 4)

| | `layout peek` | `layout create $gds` |
|--|---------------|----------------------|
| Speed / weight | Light | Heavier (full load) |
| Returns | Direct answers | A handle `$L` |
| Can call `$L bbox`? | No | Yes |

See `09_peek_vs_create.tcl`.

---

## Daily practice

| Day | Goal | Files |
|-----|------|-------|
| Day 1 | Find GDS + peek | `01`, `02`, `03` |
| Day 2 | Open + list | `04`, `05` |
| Day 3 | exists + bbox | `06`, `07`, `08` |
| Day 4 | Compare peek vs create | `09` |
| Day 5 | **Project** | `10_report_gds.tcl` |

### Week checklist

- [ ] peek cells / layers / topcell
- [ ] layout create $gds → handle
- [ ] topcell / cells / layers
- [ ] exists + bbox
- [ ] can explain peek vs create
- [ ] finished report_gds

---

## Common mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| File not found | No Week 8 GDS | `make week8-10` |
| Used peek result as `$L` | Peek is not a handle | Use `layout create` for `$L` methods |
| `exists cell` without `$L` | Need loaded layout | Open first |
| Wrong path with spaces | Path not quoted | Use `file join` |

---

## Example scripts

```bash
make week23-01
make week23
make week23-10
# optional custom file:
./scripts/run_calibre_tcl.sh lessons/23/10_report_gds.tcl -- tmp/week8_01_box.gds
```

| # | File | Practice |
|---|------|----------|
| 01 | `01_find_sample_gds.tcl` | Locate a GDS |
| 02 | `02_peek_cells_layers.tcl` | peek cells/layers/top |
| 03 | `03_peek_precision_units.tcl` | peek precision/units |
| 04 | `04_open_gds_handle.tcl` | layout create $gds |
| 05 | `05_topcell_cells_layers.tcl` | $L inventory |
| 06 | `06_exists_cell.tcl` | exists cell |
| 07 | `07_bbox_cell.tcl` | bbox |
| 08 | `08_exists_layer_and_file.tcl` | exists layer + file |
| 09 | `09_peek_vs_create.tcl` | compare modes |
| 10 | `10_report_gds.tcl` | **Week project** |
| 11 | `11_compare_two_gds.tcl` | two-file peek |
| 12 | `12_run_checklist.tcl` | Checklist |

---

## Challenge

Extend `10_report_gds.tcl`:

1. Accept a path after `--`  
2. If cell `TOP` missing, print a clear message  
3. Print whether layers `1` and `2` exist  
4. Write the report text to `tmp/week23_report.txt` using `open`/`puts`/`close` (Week 5 skill)  

---

## Looking ahead

**Week 10** — hierarchy with `$L create ref` (place one cell inside another) plus a multi-API graduation project (create + geometry + query).

---

## Parent / teacher note

- This week is read-only on drawings: no need to redraw boxes unless the GDS is missing.
- Success: child runs `make week23-10` and explains one peek line and one `$L bbox` line.
