# Tcl lessons — how to study（怎么学）

**Tcl-first** curriculum from [PLAN.md](../PLAN.md), with milestones every 10 weeks.  
Each week has bilingual notes + ≥10 runnable examples (when generated).

---

## Milestones

| Milestone | Weeks | You can… | Runtime |
|-----------|-------|----------|---------|
| **M10** | 1–10 | Read/write Tcl syntax (`$` / quotes / lists / `string` / `dict` / errors) | `tclsh` |
| **M20** | 11–20 | Fluent scripts + TclOO; pure-Tcl capstone | `tclsh` |
| **M30** | 21–30 | Calibre create / query / hierarchy / boolean | calibredrv |
| **M40** | 31–40 | Remaining batch Calibre APIs | calibredrv |

```bash
make milestones
make help
```

---

## Quick start

```bash
make help              # all targets
make week1-01          # Weeks 1–20: tclsh
make week6             # string toolkit (M10)
make week15            # TclOO
make week21-01         # first Calibre week
make help-tcl          # Tcl discovery tips
make help-calibre      # Calibre Usage tips
```

Help docs: [docs/TCL_HELP.md](../docs/TCL_HELP.md) · [docs/CALIBRE_HELP.md](../docs/CALIBRE_HELP.md) · [docs/COVERAGE.md](../docs/COVERAGE.md)

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

| Week | Folder | Topic | Runtime | Status |
|------|--------|-------|---------|--------|
| 1 | [1/](1/) | `puts`, scripts, comments | `tclsh` | ready |
| 2 | [2/](2/) | `set`, `$`, **quoting & substitution** | `tclsh` | ready |
| 3 | [3/](3/) | lists basics | `tclsh` | ready |
| 4 | [4/](4/) | `if` / loops | `tclsh` | ready |
| 5 | [5/](5/) | `proc` + files | `tclsh` | ready |
| 6 | [6/](6/) | `string` ensemble | `tclsh` | ready |
| 7 | — | lists advanced | `tclsh` | PLAN only |
| 8 | — | `dict` / `array` | `tclsh` | PLAN only |
| 9 | — | `expr` / `eval` / `subst` / `format` | `tclsh` | PLAN only |
| 10 | — | `switch` / `catch` / **M10 project** | `tclsh` | PLAN only |
| 11–14 | — | `info` / I/O / regexp / namespace | `tclsh` | PLAN only |
| 15 | [15/](15/) | TclOO basics | `tclsh` | ready |
| 16–20 | — | TclOO+ / workshops / **M20 capstone** | `tclsh` | PLAN only |
| 21 | [21/](21/) | `layout create`, handles | calibredrv | ready |
| 22 | [22/](22/) | polygon / wire / text / GDS | calibredrv | ready |
| 23 | [23/](23/) | peek / query | calibredrv | ready |
| 24 | [24/](24/) | `create ref` + Calibre graduation | calibredrv | ready |
| 25 | [25/](25/) | `$L iterator` | calibredrv | ready |
| 26 | [26/](26/) | flatten / expand | calibredrv | ready |
| 27 | [27/](27/) | filemerge / import | calibredrv | ready |
| 28 | [28/](28/) | boolean / SIZE | calibredrv | ready |
| 29–40 | — | Calibre catalog + **M40 audit** | calibredrv | PLAN only |

Missing folders: generate with the **content-generation** skill from PLAN week sections.

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

## Suggested study order right now

1. Finish **weeks 1–6** (syntax through `string`) — you are building M10.  
2. Next generate **weeks 7–10** (lists+ / dict / eval / errors) → Milestone 10.  
3. Then **11–20** (fluency + OOP) → Milestone 20.  
4. Only then start **week 21** Calibre.

Graduation GDS (Calibre): `tmp/week24_graduation.gds` — template `examples/my_graduation.tcl`.
