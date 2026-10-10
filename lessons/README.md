# Tcl lessons — how to study（怎么学）

10-week curriculum from [PLAN.md](../PLAN.md).  
Each week has bilingual notes + ≥10 runnable examples.

---

## Quick start

```bash
make help              # all targets
make week1-01          # Weeks 1–6: tclsh
make week7-01          # Weeks 7–10: calibredrv
make week10-10         # graduation project
make help-tcl          # Tcl discovery tips
make help-calibre      # Calibre Usage tips
```

Help docs: [docs/TCL_HELP.md](../docs/TCL_HELP.md) · [docs/CALIBRE_HELP.md](../docs/CALIBRE_HELP.md)

---

## If you feel lost（卡住时）

1. Run the smallest example: `make weekN-01`  
2. Read only **Concept 1** in `lesson_zh.md` (or `lesson_en.md`)  
3. Change **one** string / number, run again  
4. Check the week’s **Common mistakes** table  
5. Ask an adult to open the help doc / Calibre manual TOC  

Do **not** try to finish all 12 examples in one day. PLAN says 3–5 short sessions per week.

---

## Week map

| Week | Folder | Topic | Runtime |
|------|--------|-------|---------|
| 1 | [1/](1/) | `puts`, scripts, comments | `tclsh` |
| 2 | [2/](2/) | `set`, `$`, `expr` | `tclsh` |
| 3 | [3/](3/) | lists | `tclsh` |
| 4 | [4/](4/) | `if` / loops | `tclsh` |
| 5 | [5/](5/) | `proc` + files | `tclsh` |
| 6 | [6/](6/) | TclOO | `tclsh` |
| 7 | [7/](7/) | `layout create`, handles | calibredrv |
| 8 | [8/](8/) | polygon / wire / text / GDS | calibredrv |
| 9 | [9/](9/) | peek / query | calibredrv |
| 10 | [10/](10/) | `create ref` + graduation | calibredrv |
| 11 | [11/](11/) | `$L iterator` (optional advanced) | calibredrv |

Each week: `lesson_en.md` + `lesson_zh.md` + `01_*.tcl` … `12_*.tcl`.

---

## Suggested path for one week

| Day | Do this |
|-----|---------|
| 1 | Read Big idea + Concept 1; run `01`–`02` |
| 2 | Concepts 2–3; run `03`–`05` |
| 3 | Practice; run mid examples |
| 4 | Common mistakes; re-run anything that failed |
| 5 | Week project (`10_*.tcl`) |

---

## After Week 10

See PLAN appendix: iterators, filemerge, booleans, RDB, GUI macros, your own tool library.  
Graduation GDS: `tmp/week10_graduation.gds` — optional copy of script: `examples/my_graduation.tcl`.
