# Week 24 — Hierarchy: `create ref` + Multi-API Capstone

> Part of the [10-week Tcl learning plan](../../PLAN.md).  
> Goal this week: place cells with `$L create ref`, then finish a graduation script that combines **create + geometry + query**.

**Environment:** Calibre DESIGNrev. Help: [docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md).

---

## Learning goals

By the end of this week, you should be able to:

1. Explain **create ref**: put one cell (part) inside another cell (room).
2. Write `$L create ref incell refcell x y mirror angle mag`.
3. Use optional **array** args: `cols rows xspace yspace`.
4. Query hierarchy with `$L children` (and peek / bbox as in Week 9).
5. Finish a **graduation project** that uses:
   - ≥1 create API (`layout create`, `create cell` / `layer`)
   - ≥2 geometry APIs (`polygon` / `text` / `wire`)
   - `$L create ref`
   - `gdsout` + ≥2 query APIs (`peek`, `cells`, `bbox`, …)
6. Name three APIs you used, out loud.

This is the last week of the 10-week plan.

---

## Big idea

| Idea | Everyday metaphor | Tcl |
|------|-------------------|-----|
| Leaf cell | A brick / LEGO piece | `create cell BOX` + polygon |
| Parent cell | The play table / house | `create cell TOP` |
| `create ref` | Stamp the brick onto the table | `$L create ref TOP BOX x y …` |
| Array ref | Stamp many bricks in a grid | extra `cols rows xspace yspace` |

You still use Week 7–9 skills: handle `$L`, draw shapes, ask questions.

---

## Concept 1 — `create ref` syntax

```tcl
$L create ref TOP BOX 0 0 0 0 1
#               ^    ^   ^ ^ ^ ^ ^
#               |    |   | | | | mag (scale)
#               |    |   | | | angle
#               |    |   | | mirror (0 = no)
#               |    |   x y
#               |    cell being placed
#               parent cell (where we place)
```

Usage from Calibre help:

`create ref <incell> <refcell> <x> <y> <mirror> <angle> <mag> [<cols> <rows> <xspace> <yspace>]`

See `03_create_ref_once.tcl`, `04_create_ref_two.tcl`.

---

## Concept 2 — Array placement

```tcl
# 2 cols x 2 rows, spacing 15
$L create ref GRID DOT 0 0 0 0 1 2 2 15 15
```

See `05_create_ref_array.tcl`.

---

## Concept 3 — Children after refs

```tcl
puts [$L children TOP]
```

Often lists the cells placed into `TOP` (for example `BOX`).

See `07_report_hierarchy.tcl`.

---

## Concept 4 — Graduation projects (pick one)

From PLAN:

1. Two-layer house + text + report  
2. Brick array with `create ref`  
3. Letter made of polygons / refs  
4. (Bonus) TclOO factory wrapping `$L`  
5. (Parent optional) GUI `cwbWorkBench`

Default example in this folder: **brick array** → `10_graduation_project.tcl`.

Optional OOP version: `11_oop_layout_factory.tcl`.

---

## Daily practice

| Day | Goal | Files |
|-----|------|-------|
| Day 1 | Plan APIs on paper | `01_api_plan_checklist.tcl` |
| Day 2 | Leaf cell + one ref | `02`, `03` |
| Day 3 | Two refs / array / house | `04`, `05`, `06` |
| Day 4 | Report + combo | `07`, `08`, `09` |
| Day 5 | **Graduation** | `10_graduation_project.tcl` |

### Week checklist

- [ ] I understand create ref  
- [ ] create + cell/layer  
- [ ] ≥2 geometry APIs  
- [ ] create ref used  
- [ ] gdsout succeeded  
- [ ] ≥2 query APIs  
- [ ] I can name 3 APIs out loud  

---

## Common mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| ref before leaf exists | Placed missing cell | Create `BOX` (with geometry) first |
| Wrong argument order | Mixed x/y/mirror/angle/mag | Copy PLAN sample order |
| Only TOP in peek cells | Leaf may still appear in `$L cells` | Check `$L cells` and `$L children` |
| Forgot gdsout TOP | Exported wrong cell | `$L gdsout file TOP` |

---

## Example scripts

```bash
make week24-01
make week24
make week24-10
```

| # | File | Practice |
|---|------|----------|
| 01 | `01_api_plan_checklist.tcl` | Plan APIs |
| 02 | `02_leaf_cell_box.tcl` | Leaf BOX |
| 03 | `03_create_ref_once.tcl` | One ref |
| 04 | `04_create_ref_two.tcl` | PLAN two refs |
| 05 | `05_create_ref_array.tcl` | 2×2 array |
| 06 | `06_two_layer_house.tcl` | House project idea |
| 07 | `07_report_hierarchy.tcl` | Query hierarchy |
| 08 | `08_ref_then_peek.tcl` | Build + peek |
| 09 | `09_mini_combo.tcl` | Mini multi-API |
| 10 | `10_graduation_project.tcl` | **Capstone** |
| 11 | `11_oop_layout_factory.tcl` | TclOO bonus |
| 12 | `12_run_checklist.tcl` | Checklist |

---

## Challenge

1. Change the graduation array to **4×3** bricks.  
2. Add your initials as `create text`.  
3. Copy the finished script to `examples/my_graduation.tcl`.  
4. Show a parent: run `make week24-10` and name three APIs.

---

## Looking ahead (after Week 24)

See PLAN appendix: iterators, filemerge, boolean ops, RDB, GUI macros, your own TclOO tool library.

---

## Parent / teacher note

- Graduation success = script runs + GDS exists + child can name create / geometry / query APIs.  
- GUI viewing is optional.  
- OOP factory (`11`) is bonus only.
