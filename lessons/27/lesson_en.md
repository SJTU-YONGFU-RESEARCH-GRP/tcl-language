# Week 27 — Stitching Layouts: `layout filemerge` / `$L import layout`

> Optional advanced week after the [10-week plan](../../PLAN.md).  
> Goal: combine two small GDS files into one kit — on disk (`filemerge`) and in memory (`import layout`).

**Environment:** Calibre DESIGNrev. Help: [docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md).

---

## Learning goals

1. Build two input GDS files with different cell names.
2. Merge with `layout filemerge -in … -in … -out …`.
3. Use `-createtop`, `-mode rename`, and `-infile` + `-placecell`.
4. Call `$L import layout $src 0 append` (and know what `del=1` does).
5. Finish **merge_kit**: `tmp/week27_kit.gds` + `tmp/week27_report.txt`.

---

## Big idea

| Tool | Where it works | Metaphor |
|------|----------------|----------|
| `layout filemerge` | Files on disk | Staple two notebooks into one book |
| `$L import layout` | Memory handles | Pour one tray of LEGO into another tray |
| `layout copy` | Memory | Photocopy a tray before you experiment |

---

## Prerequisites

- Weeks 8–10: cells, polygons, GDS out/in
- Week 11–12: iterators / refs (useful to check results)
- Calibre via `./scripts/run_calibre_tcl.sh`

---

## Concept 1 — Two inputs

Different cell names make the first merge easy (`LEFT` + `RIGHT`).

See `01_build_two_gds.tcl`.

---

## Concept 2 — Basic `filemerge`

```tcl
layout filemerge -in left.gds -in right.gds -out merged.gds
```

- Always use `-in` / `-out` (bare filenames alone fail).
- Open the result: `layout create merged.gds -dt_expand` then `$M cells`.

See `02_filemerge_usage.tcl`, `03_filemerge_basic.tcl`.

---

## Concept 3 — `-createtop` and conflict modes

```tcl
layout filemerge -in a.gds -in b.gds -out out.gds -createtop CHIP
layout filemerge -in t1.gds -in t2.gds -out out.gds -mode rename
```

| Flag | Meaning |
|------|---------|
| `-createtop CHIP` | New top cell; children hang under it |
| `-mode append` | Same name → combine shapes (default-ish) |
| `-mode overwrite` | Same name → keep later file’s cell |
| `-mode rename` | Same name → rename one (e.g. `TOP_WB1`) |

Do **not** pass both `-mode rename` and a bare `-overwrite` flag — Calibre says “specify only one mode.”

See `04_createtop.tcl`, `05_mode_rename.tcl`.

---

## Concept 4 — Place while merging

```tcl
layout filemerge \
    -infile {-name left.gds  -placecell {-refcell LEFT  -x 0  -y 0}} \
    -infile {-name right.gds -placecell {-refcell RIGHT -x 50 -y 0}} \
    -out placed.gds \
    -createtop CHIP
```

Refs appear under `CHIP` at the coordinates you chose.

See `06_placecell.tcl`.

---

## Concept 5 — `$L import layout`

Working form on this machine:

```tcl
$L import layout $src 0 append
#                 ^handle  ^del  ^mode
```

| Argument | Values | Meaning |
|----------|--------|---------|
| `$src` | layout handle | Source to pull from |
| `$del` | `0` or `1` | `0` = keep source; `1` = destroy source after import |
| `$mode` | `append` / `overwrite` / `rename` | Same-name cell policy |

Wrong arity prints Usage; a numeric “mode” fails with “valid modes = {append, overwrite, rename}”.

See `07_import_layout.tcl`, `08_import_del_modes.tcl`, `11_import_usage_hint.tcl`.

---

## Concept 6 — `layout copy` (helper)

```tcl
set dup [layout copy $src]
```

In-memory photocopy — handy before risky edits. See `09_layout_copy.tcl`.

---

## Daily practice

| Day | Goal | Files |
|-----|------|-------|
| 1 | Two GDS inputs | `01`, `02` |
| 2 | Basic filemerge | `03` |
| 3 | createtop / rename / placecell | `04`, `05`, `06` |
| 4 | import layout | `07`, `08`, `11` |
| 5 | **merge_kit** | `10` |

### Checklist

- [ ] `-in` / `-out` filemerge  
- [ ] `-createtop` / `-mode rename`  
- [ ] `-infile` + `-placecell`  
- [ ] `import layout` with `del` + `mode`  
- [ ] Kit GDS + report written  

---

## Common mistakes

| Symptom | Fix |
|---------|-----|
| `Unknown option file.gds` | Need `-in file.gds`, not bare path |
| `Please specify only one mode` | Use `-mode rename` **or** `-overwrite`, not both |
| `valid modes = {append,…}` | Third arg must be a mode **name**, not `0` |
| Source handle gone | You used `del=1` — reopen GDS or use `del=0` |

---

## Example scripts

```bash
make week27-01
make week27
make week27-10
```

| # | File | Focus |
|---|------|-------|
| 01 | `01_build_two_gds.tcl` | Inputs |
| 02 | `02_filemerge_usage.tcl` | Usage |
| 03 | `03_filemerge_basic.tcl` | Basic merge |
| 04 | `04_createtop.tcl` | `-createtop` |
| 05 | `05_mode_rename.tcl` | `-mode rename` |
| 06 | `06_placecell.tcl` | Placed stitch |
| 07 | `07_import_layout.tcl` | import basics |
| 08 | `08_import_del_modes.tcl` | del + modes |
| 09 | `09_layout_copy.tcl` | `layout copy` |
| 10 | `10_merge_kit.tcl` | **project** |
| 11 | `11_import_usage_hint.tcl` | Wrong arity |
| 12 | `12_run_checklist.tcl` | Checklist |

---

## Challenge

Merge three blocks with `-placecell` at `(0,0)`, `(40,0)`, `(0,40)` under top cell `CITY`, then print all refs with `iterator ref`.

---

## Looking ahead

Next optional week: [Week 14 — AND / OR / NOT / SIZE](../14/lesson_en.md). Then RDB, GUI macros.

---

## Parent / teacher note

Optional week. Success: `make week27-10` writes `tmp/week27_kit.gds` and a short report. Uses calibredrv.
