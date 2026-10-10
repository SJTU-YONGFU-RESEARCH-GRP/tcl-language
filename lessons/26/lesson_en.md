# Week 26 — Hierarchy Flatten: `$L flatten` / `expand ref`

> Optional advanced week after the [10-week plan](../../PLAN.md).  
> Goal: turn “refs to other cells” into real polygons on this cell.

**Environment:** Calibre DESIGNrev. Help: [docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md).

---

## Learning goals

1. Build a small hierarchy: BOX with a polygon; TOP with two `create ref` instances.
2. Run `$L flatten cell TOP` and see refs disappear, polygons appear on TOP.
3. Use `-withDelete` and notice unused child cells leave `$L cells`.
4. Expand **one** instance with `$L expand ref` (or `flatten ref`) using matching placement.
5. Finish **flatten_report**: write before/after stats to `tmp/week26_report.txt`.

---

## Big idea

| Week 10 | Week 26 |
|---------|----------|
| Place stamps (`create ref`) | Peel stamps into real ink on the page |
| Hierarchy stays nested | Flatten = one flat drawing |

Everyday metaphor: a Lego instruction sheet names brick kits. **Flatten** draws every brick outline on one big paper. **Expand one ref** peels only the kit sitting at one spot on the table.

---

## Prerequisites

- Week 8: `create cell` / `create layer` / `create polygon`
- Week 10: `create ref`
- Week 11: `iterator poly` / `iterator ref` (handy for before/after checks)
- Calibre via `./scripts/run_calibre_tcl.sh` (parent/teacher: `./scripts/setup_calibredrv.sh`)

---

## Concept 1 — Hierarchy before flatten

```tcl
$L create cell BOX
$L create polygon BOX 1_0 0 0 10 10
$L create cell TOP
$L create ref TOP BOX 0 0 0 0 1
$L create ref TOP BOX 20 0 0 0 1
```

Typical snapshot:

| Query | Before flatten |
|-------|----------------|
| `$L children TOP` | `BOX` |
| `iterator ref TOP` | 2 refs |
| `iterator poly TOP 1 …` | 0 |
| `iterator poly BOX 1 …` | 1 |

See `01_build_hierarchy.tcl`, `03_before_snapshot.tcl`.

---

## Concept 2 — `$L flatten cell TOP`

```tcl
$L flatten cell TOP
```

Usage (from Calibre): `flatten cell <cellname> [-withDelete]`.

After flatten (no `-withDelete`):

- refs on TOP → gone
- polygons on TOP → usually **2** (one per former instance, shifted by placement)
- cell `BOX` may still exist in `$L cells`

Sample idea of coordinates:

```
{0 0 10 0 10 10 0 10}     ;# instance at (0,0)
{20 0 30 0 30 10 20 10}    ;# instance at (20,0)
```

See `04_flatten_cell.tcl`, `09_coords_after_flatten.tcl`.

---

## Concept 3 — `-withDelete`

```tcl
$L flatten cell TOP -withDelete
```

Same as flatten, then delete child cells that nobody references anymore. Often `$L cells` becomes just `TOP`.

See `05_with_delete.tcl`.

---

## Concept 4 — One instance: `expand ref` / `flatten ref`

You must **already** have a matching `create ref`. Then:

```tcl
$L expand ref TOP BOX 0 0 0 0 1
# same placement args as create ref: incell refcell x y mirror angle mag
```

- Expands **only** that instance.
- Other refs stay.
- On this machine `flatten ref …` with the same args behaves the same.

If no matching sref exists, Calibre errors — catch it and create the ref first (`11_need_existing_ref.tcl`).

See `06_expand_one_ref.tcl`, `07_flatten_ref_same.tcl`, `08_compare_cell_vs_ref.tcl`.

---

## Concept 5 — Usage hint

Incomplete calls print Usage:

```tcl
catch {$L flatten} msg   ;# layoutN flatten <cell|ref|aref> ...
catch {$L expand} msg    ;# layoutN expand <cell|ref> ...
```

See `02_flatten_usage_hint.tcl`.

---

## Daily practice

| Day | Goal | Files |
|-----|------|-------|
| 1 | Build hierarchy + before snapshot | `01`, `02`, `03` |
| 2 | `flatten cell` | `04`, `09` |
| 3 | `-withDelete` | `05` |
| 4 | One-ref expand / flatten | `06`, `07`, `08` |
| 5 | **flatten_report** | `10` |

### Checklist

- [ ] Build BOX + TOP refs  
- [ ] `flatten cell TOP`  
- [ ] `-withDelete`  
- [ ] `expand ref` / `flatten ref` one instance  
- [ ] `tmp/week26_report.txt` written  

---

## Common mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `unable to expand ref` | No matching `create ref` | Create ref with same x/y/mirror/angle/mag first |
| Still 0 polys on TOP | Forgot flatten / wrong cell | Call `flatten cell TOP` then `iterator poly` |
| `BOX` still in `cells` | No `-withDelete` | Add `-withDelete` if you want unused cells gone |
| `Unrecognized type arg (TOP)` | Wrote `flatten TOP` | Need `flatten cell TOP` |

---

## Example scripts

```bash
make week26-01
make week26
make week26-10
```

| # | File | Focus |
|---|------|-------|
| 01 | `01_build_hierarchy.tcl` | BOX + two refs → GDS |
| 02 | `02_flatten_usage_hint.tcl` | Usage messages |
| 03 | `03_before_snapshot.tcl` | Inventory before |
| 04 | `04_flatten_cell.tcl` | `flatten cell` |
| 05 | `05_with_delete.tcl` | `-withDelete` |
| 06 | `06_expand_one_ref.tcl` | One `expand ref` |
| 07 | `07_flatten_ref_same.tcl` | `flatten ref` parity |
| 08 | `08_compare_cell_vs_ref.tcl` | Cell vs one ref |
| 09 | `09_coords_after_flatten.tcl` | Shifted coords |
| 10 | `10_flatten_report.tcl` | **project** |
| 11 | `11_need_existing_ref.tcl` | Error without ref |
| 12 | `12_run_checklist.tcl` | Checklist |

---

## Challenge

Add a third ref at `(0,20)`, flatten only that one with `expand ref`, leave the other two as refs, and print the remaining `iterator ref` list.

---

## Looking ahead

Next optional week: [Week 13 — filemerge / import layout](../13/lesson_en.md). Then boolean ops (`AND`/`OR`/`NOT`/`SIZE`), RDB, GUI macros.

---

## Parent / teacher note

Optional week. Success: child runs `make week26-10` and opens `tmp/week26_report.txt` (before/after counts make sense). Uses calibredrv, not plain `tclsh`.
