# Week 7 — Getting Started + `layout create` and Handles

> Part of the [10-week Tcl learning plan](../../PLAN.md).  
> Goal this week: run Calibre scripts, understand **handles**, use empty and file-based layouts.

---

## Learning goals

By the end of this week, you should be able to:

1. Run a script with `./scripts/run_calibre_tcl.sh lessons/7/....tcl` (batch mode).
2. Explain **handle（句柄）**: a Tcl name for a Calibre layout object.
3. Use `set L [layout create]` to make an empty layout.
4. Use `set L [layout create $gds]` to open an existing GDS file.
5. Call `$L create cell TOP` and `$L create layer ...` on a handle.
6. Connect Week 6 OOP to Calibre: `Pet new` ↔ `layout create`, `$cat speak` ↔ `$L create cell`.
7. Finish `10_my_hello_layout.tcl`: self-intro + empty layout + print handle.

**Environment:** Calibre DESIGNrev required. Parent/teacher runs `./scripts/setup_calibredrv.sh` (included in `run_calibre_tcl.sh`).

---

## Big idea (wear your Week 6 OOP glasses)

| Week 6 TclOO | Week 7 Calibre | Meaning |
|--------------|----------------|---------|
| `oo::class create Pet` | (Calibre provides layout) | The "mold" is built-in |
| `[Pet new "Mimi"]` | `[layout create]` | Make a new object |
| `$cat speak` | `$L create cell TOP` | Tell the object to do something |
| handle in `$cat` | handle in `$L` | Variable stores the object ticket |

Calibre manual: **Tcl Objects Have Handles** — `layout create` returns a handle; you store it and call `$L method ...`.

---

## Three API categories (map for weeks 7–10)

| Category | Looks like | Does what | This week |
|----------|------------|-----------|-----------|
| A. layout commands | `layout create`, `layout peek` | Create / peek at files | **Yes** |
| B. Layout object methods | `$L create polygon ...` | Draw and query on one layout | Start (cell, layer) |
| C. GUI / Workbench | `cwbWorkBench` | Control open GUI | Week 10 optional |

---

## How to run (not plain `tclsh`)

| Mode | Command | Your role |
|------|---------|-----------|
| **Batch script** | `make week7-01` or `./scripts/run_calibre_tcl.sh lessons/7/01_....tcl` | **Main way** |
| View GDS in GUI | `./scripts/open_gds.sh tmp/week7_script1.gds` (with VNC) | Parent helps verify |
| Interactive | `calibredrv -shell` | Optional play |

From project root:

```bash
make week7-02
make week7
make list WEEK=7
```

---

## Concept 1 — Hello from calibredrv (Day 2)

Same `puts` as Week 1, but inside Calibre's Tcl:

```tcl
puts "hello from calibredrv Tcl"
puts "tcl_version=$tcl_version"
exit
```

Always end batch scripts with `exit` so calibredrv closes cleanly.

See `01_hello_calibredrv.tcl` and `examples/hello_calibre.tcl`.

---

## Concept 2 — `layout create` and the handle (Day 3)

```tcl
set L [layout create]
puts "Handle L = $L"
```

Expected output (example):

```text
Handle L = layout0
```

The exact name (`layout0`, `layout1`, …) is assigned by Calibre. **Your job:** save it in `L` and use `$L` for every following command.

### Handle in one sentence

A **handle** is a short ticket Tcl uses to talk to one layout object in memory.

---

## Concept 3 — Object methods: `$L create cell` (Day 4–5)

Official Script 1 skeleton:

```tcl
set L [layout create]
$L create cell TOP
$L create layer 1
$L create layer 2.7
$L create polygon TOP 1_0 0 0 100 100
$L gdsout temp.gds
```

This week: focus on **create** through layers. Full polygon + GDS detail is Week 8.

| Command | Plain English |
|---------|---------------|
| `$L create cell TOP` | Add a cell named TOP |
| `$L create layer 1` | Add layer 1 |
| `$L create layer 2.7` | Layer 2, datatype 7 |

See `04_create_cell_top.tcl`, `05_create_layers.tcl`, `07_script1_skeleton.tcl`.

---

## Concept 4 — Open layout from file (Day 4–5)

```tcl
set L [layout create $gds]
puts "Opened: $L"
```

Optional flag (keep layer/datatype separate):

```tcl
set L [layout create $gds -dt_expand]
```

See `08_layout_create_from_gds.tcl`, `09_layout_dt_expand.tcl`.

---

## Concept 5 — OOP comparison table (Day 4)

Draw this in your notebook:

```
Pet new              ↔  layout create
$cat speak           ↔  $L create cell TOP
object.method        ↔  $L gdsout file.gds
```

See `06_oop_comparison.tcl`.

---

## Daily practice

| Day | Goal | Files |
|-----|------|-------|
| Day 1 | Setup + find `layout create` in manual TOC | (with parent) |
| Day 2 | Run hello script | `01_hello_calibredrv.tcl` |
| Day 3 | Empty layout + handle | `02_layout_create_empty.tcl`, `03_handle_explain.tcl` |
| Day 4 | cell, layers, OOP link | `04`–`06`, `08` |
| Day 5 | **Project** | `10_my_hello_layout.tcl` |

Also run: `07_script1_skeleton.tcl` (writes `tmp/week7_script1.gds`).

### Week checklist

- [ ] I can run `./scripts/run_calibre_tcl.sh` scripts.
- [ ] I can explain handle in my own words.
- [ ] I used `layout create` (empty and from file).
- [ ] I called `$L create cell TOP`.
- [ ] I linked OOP ideas to `$L` commands.
- [ ] I finished `10_my_hello_layout.tcl`.

---

## Common mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `invalid command name "layout"` | Ran with `tclsh` not calibredrv | Use `make week7-NN` or `run_calibre_tcl.sh` |
| Forgot `$` on handle | Wrote `L create cell` | Use `$L create cell TOP` |
| Script hangs at end | No `exit` | Add `exit` at bottom |
| GDS open fails | File missing | Run `make week7-07` first |
| Confused handle value | Expected a file path | Handle is like `layout0`, not a path |

---

## Example scripts

```bash
make week7-01
make week7
make run WEEK=7 EX=10
```

| # | File | Practice |
|---|------|----------|
| 01 | `01_hello_calibredrv.tcl` | Hello in calibredrv |
| 02 | `02_layout_create_empty.tcl` | Empty layout |
| 03 | `03_handle_explain.tcl` | Handle story |
| 04 | `04_create_cell_top.tcl` | `$L create cell` |
| 05 | `05_create_layers.tcl` | Layers 1 and 2.7 |
| 06 | `06_oop_comparison.tcl` | OOP ↔ Calibre |
| 07 | `07_script1_skeleton.tcl` | Script 1 + GDS out |
| 08 | `08_layout_create_from_gds.tcl` | Open GDS |
| 09 | `09_layout_dt_expand.tcl` | `-dt_expand` |
| 10 | `10_my_hello_layout.tcl` | **Week project** |
| 11 | `11_two_layouts_two_handles.tcl` | Two handles |
| 12 | `12_run_checklist.tcl` | Checklist |

---

## Challenge

Customize `10_my_hello_layout.tcl`:

1. Your real name and goal  
2. Create two cells: `TOP` and `SUB`  
3. Print both handles if you make two layouts (`11` as hint)  
4. Run `07` first, then open GDS with parent help  
5. Four `#` comments: intro, handle, cell, exit  

---

## Looking ahead

**Week 8** — create geometry in detail: polygon, wire, text, and write GDS. You already saw `$L create polygon` in `07_script1_skeleton.tcl`.

---

## Parent / teacher note

- Manual: `calbr_drv_ref` — Introduction + Getting Started + Writing Layout Viewer Scripts.
- Batch runs need license + `setup_calibredrv.sh`; GUI viewing is optional via VNC.
- Success: child runs `make week7-10`, reads handle from output, explains it like a "object ticket."
