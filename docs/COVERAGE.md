# Command coverage map — tclsh + calibredrv

> Master checklist for [PLAN.md](../PLAN.md) (**Tcl-first**, milestones 10 / 20 / 30 / 40).  
> Status: `done` | `planned` | `bonus` | `phaseC` | `skip`

Refresh Tcl side anytime:

```bash
tclsh -c 'foreach c [lsort [info commands]] {puts $c}'
```

Calibre Layout Object names come from the official TOC:  
`.../htmldocs/calbr_drv_ref/calbr_drv_ref_toc.html` → **Layout Object**.

---

## Paths (milestones)

| Path | Weeks | Goal |
|------|-------|------|
| **M10** Tcl syntax | 1–10 | puts → string / lists+ / dict / eval / errors |
| **M20** fluency + OOP | 11–20 | info / I/O / regexp / namespace / TclOO + pure-Tcl capstone |
| **M30** Calibre core | 21–30 | layout create … boolean + catalog start |
| **M40** Calibre catalog | 31–40 | remaining batch API + coverage audit |
| Phase C | later | `cwbWorkBench` / Writing Macros（GUI） |

### Old → new week map

| Old | New | Topic |
|-----|-----|-------|
| 1–5 | 1–5 | foundation (week 2 now emphasizes quoting) |
| 6 TclOO | **15** | TclOO basics |
| 7–14 Calibre | **21–28** | Calibre core + advanced |
| 15–19 Catalog A | **6–10** | string … errors (M10) |
| 20–24 Catalog A | **11–14, 16** | info … namespace, TclOO+ |
| 25–40 Catalog B | **29–40** | Calibre encyclopedia |

---

## Tcl — top-level commands (`info commands`)

| Command | Status | Week |
|---------|--------|------|
| `puts` | done | 1 |
| `exit` | done | 1 |
| `set` | done | 2 |
| quoting / `$` / `[]` / `""` / `{}` | done / deepen | **2** |
| `expr` | done / deepen | 2 / **9** |
| `list` `lindex` `llength` `lappend` | done | 3 |
| `if` `for` `foreach` `while` `incr` | done | 4 |
| `proc` `return` `open` `close` `gets` `file` (basics) | done | 5 |
| `string` (all subcommands) | done | **6** |
| `lrange` `lsearch` `lsort` `linsert` `lreplace` `lmap` `lassign` `lreverse` `lrepeat` `lset` `join` `split` `concat` | planned | **7** |
| `dict` `array` | planned | **8** |
| `append` `unset` `subst` `eval` `format` `scan` | planned | **9** |
| `switch` `catch` `try` `throw` `error` `break` `continue` | planned | **10** |
| `info` | planned | **11** |
| `chan` `read` `seek` `tell` `glob` `pwd` `cd` `source` `exec` `pid` `flush` `eof` | planned | **12** |
| `regexp` `regsub` `clock` | planned | **13** |
| `namespace` `package` `apply` `rename` `trace` | planned | **14** |
| `oo::class` `oo::define` (basics) | done | **15** |
| TclOO advanced (`oo::copy` `oo::objdefine` …) | planned | **16** |
| scripting patterns / modules | planned | **17** |
| review workshops | planned | **18–19** |
| pure-Tcl capstone | planned | **20** |
| `binary` `zlib` `encoding` | bonus | 12/14 appendix |
| `socket` `coroutine` `yield` `interp` `vwait` `update` `after` `fileevent` | bonus | power-tools |
| `global` `upvar` `uplevel` `variable` | planned | 14 (with namespace) |
| `history` `time` `load` `unload` `unknown` | bonus / skip | rarely needed |
| `auto_*` `tclLog` `case` | skip | legacy / internal |
| `fblocked` `fconfigure` `fcopy` | planned | 12 (via `chan`) |

### Ensembles

| Ensemble | Week |
|----------|------|
| `file` (full) | 5 basics + **12** deep |
| `string` | **6** |
| `dict` / `array` | **8** |
| `info` | **11** |
| `chan` | **12** |
| `clock` | **13** |
| `namespace` / `package` | **14** |

---

## Calibre — global `layout`

| Subcommand | Status | Week |
|------------|--------|------|
| `layout create` | done | **21** |
| `layout peek` | done / catalog deep | **23** / **39** |
| `layout filemerge` | done | **27** |
| `layout copy` `layout merge` | done (light) / catalog | **27** / **29** |
| `layout all` `delete` `copy2` `droasis` `filtershapes` `overlays` `tbmode` | planned | **29** |

---

## Calibre — Layout Object (`$L …`)

| API | Status | Week |
|-----|--------|------|
| `create cell\|layer\|polygon\|wire\|text` | done | **22** |
| `create ref` | done | **24** |
| `gdsout` | done | **22** |
| `exists` `bbox` `cells` `children` `layers` | done | **23** |
| `query` | done | **23** |
| `iterator` (poly/wire/text/ref) | done | **25** |
| `flatten` / `expand` | done | **26** |
| `import layout` | done | **27** |
| `AND` `OR` `NOT` `XOR` `SIZE` | done | **28** |
| `oasisout` (light) | catalog deep | 22 / **37** |
| `units` / `precision` | done light / catalog | 22 / **30** |
| `allowupdates` `holdupdates` `update` | planned | **40** |
| `ancestors` `maxdepth` `refcount` `isReferenced` `duplicate cell` `cellname` `topcell` `viacell` | planned | **31** |
| `clips` `clipsout` `create clip` `rdbout` | planned | **36** |
| `connect` `disconnect` `stopconnect` `extractNet` | planned | **38** |
| `COPY` `COPYCELL GEOM` `modify origin` `modify text` `scale` `SNAP` `gridsnap` | planned | **34** |
| `delete *` family | planned | **33** |
| `layernames` `layerconfigure` … | planned | **32** |
| `iterator count *` | planned | **35** |
| `asciiout` `textout` `instancedbout` `report` | planned | **37** |
| `file` `format` `layoutType` `libname` `readonly` `ismodified` `options` | planned | **30** |
| `property` `srefsFromAref` `info` | planned | **40** |
| `transcript*` `pushmarkers` `ruler` | planned | **40** |
| `isOverlay` | planned | **40** |

---

## Overlay / Peek / GUI

| Area | Status | Week |
|------|--------|------|
| Peek object options (full) | planned | **39** |
| `overlay *` + overlay object | planned | **40** |
| `cwbWorkBench` / macros | phaseC | Phase C |

---

## Lesson folder status

| Week | Folder | Notes |
|------|--------|-------|
| 1–6 | `lessons/1` … `6` | M10 start (6 = string) |
| 7–14 | planned | generate via content-generation |
| 15 | `lessons/15` | TclOO basics |
| 16–20 | planned | M20 remainder |
| 21–28 | `lessons/21` … `28` | Calibre core (ex 7–14) |
| 29–40 | planned | Catalog B |
| Phase C | not started | after 40 |
