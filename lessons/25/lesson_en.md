# Week 25 — Walking Shapes: `$L iterator` (poly / wire / text)

> Optional advanced week after the [10-week plan](../../PLAN.md).  
> Goal: list every polygon, wire, and text on a cell/layer — not only “which layers exist.”

**Environment:** Calibre DESIGNrev. Help: [docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md).

---

## Learning goals

1. Call `$L iterator poly TOP 1 range 0 end` and get a list of coordinate groups.
2. Do the same for `wire` and `text`.
3. Use `foreach` to print each shape.
4. Explain: `$L layers` = inventory; `iterator` = details on a sheet.
5. Finish **dump_shapes**: write a text report of all shapes to `tmp/week25_dump.txt`.

---

## Big idea

| Week 9 | Week 25 |
|--------|----------|
| “What rooms / sheets exist?” | “What drawings are *on* this sheet?” |
| `$L layers` → `1 2` | iterator → each polygon’s coordinates |

Everyday metaphor: Week 9 counts colored papers; Week 25 reads every doodle on paper #1.

---

## Concept 1 — Syntax (from Calibre Usage)

```
$L iterator {wire|poly|text} <cell> <list of layers> range <l> <h> ...
```

Working pattern on this machine:

```tcl
set polys [$L iterator poly TOP 1 range 0 end]
set wires [$L iterator wire TOP 2 range 0 end]
set texts [$L iterator text TOP 1 range 0 end]
```

- `range 0 end` means “from the first to the last.”
- Layer can be `1` or `{1}` (both work here).

See `02_iterator_usage_hint.tcl`, `03_iterator_poly.tcl`.

---

## Concept 2 — `foreach` the results

```tcl
foreach p $polys {
    puts "coords = $p"
}
```

Each `$p` is one shape’s data (coordinates or text payload).

See `04_foreach_poly.tcl`.

---

## Concept 3 — Inventory vs details

```tcl
puts [$L layers]                          ;# which layers
set n [llength [$L iterator poly TOP 1 range 0 end]]  ;# how many polys on L1
```

See `07_layers_vs_iterator.tcl`.

---

## Daily practice

| Day | Goal | Files |
|-----|------|-------|
| 1 | Build sample + poly iterator | `01`, `02`, `03` |
| 2 | wire + text | `05`, `06` |
| 3 | foreach + counts | `04`, `08` |
| 4 | Compare to Week 9 | `07`, `09` |
| 5 | **dump_shapes** | `10` |

### Checklist

- [ ] iterator poly  
- [ ] iterator wire / text  
- [ ] foreach print  
- [ ] layers vs iterator  
- [ ] dump_shapes done  

---

## Common mistakes

| Symptom | Fix |
|---------|-----|
| `Not enough arguments` | Need cell + layer + `range lo hi` |
| No week25_shapes.gds | `make week25-01` |
| Empty list on a layer | Wrong layer number — check `$L layers` |

---

## Example scripts

```bash
make week25-01
make week25
make week25-10
```

| # | File | Focus |
|---|------|-------|
| 01 | `01_build_sample_shapes.tcl` | Known shapes GDS |
| 02 | `02_iterator_usage_hint.tcl` | Usage message |
| 03 | `03_iterator_poly.tcl` | poly |
| 04 | `04_foreach_poly.tcl` | foreach |
| 05 | `05_iterator_wire.tcl` | wire |
| 06 | `06_iterator_text.tcl` | text |
| 07 | `07_layers_vs_iterator.tcl` | compare |
| 08 | `08_count_all_shapes.tcl` | census |
| 09 | `09_iterator_on_week8_gds.tcl` | old homework |
| 10 | `10_dump_shapes.tcl` | **project** |
| 11 | `11_iterator_ref_bonus.tcl` | ref bonus |
| 12 | `12_run_checklist.tcl` | checklist |

---

## Looking ahead

Next optional week: [Week 12 — flatten / expand ref](../12/lesson_en.md). Then filemerge, boolean ops, RDB, GUI macros.

---

## Parent / teacher note

Optional week. Success: child runs `make week25-10` and opens `tmp/week25_dump.txt`.
