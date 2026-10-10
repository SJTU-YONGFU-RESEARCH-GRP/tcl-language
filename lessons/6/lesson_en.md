# Week 6 — String Toolkit: `string`

> Part of [PLAN.md](../../PLAN.md) **M10** (weeks 1–10).  
> Goal: use the full `string` ensemble — length, slice, case, trim, find, map.  
> Coverage: [docs/COVERAGE.md](../../docs/COVERAGE.md).

**Environment:** plain `tclsh` (`make week6`).

---

## Learning goals

1. Measure and slice with `length` / `index` / `range`.
2. Change case and trim whitespace.
3. Find and compare with `first` / `last` / `match` / `equal` / `compare`.
4. Transform with `map` / `replace` / `repeat` / `reverse` / `cat`.
5. Finish **string_toolkit**: clean a messy line → `tmp/week6_toolkit.txt`.

---

## Big idea

| Everyday | Tcl |
|----------|-----|
| Count letters | `string length` |
| Cut a piece | `string range` |
| Uppercase sticker | `string toupper` |
| Erase edge spaces | `string trim` |
| Find a letter | `string first` |
| Swap words | `string map` |

---

## Prerequisites

Weeks 1–5 (`puts`, `set`, lists, control, `proc`). Continue deepening Tcl syntax (M10).

---

## Concept 1 — Length, index, range

```tcl
string length "Hello"       ;# 5
string index  "ABC" 0       ;# A
string range  "ABCDEF" 1 3  ;# BCD
```

See `01_string_length.tcl`, `02_index_range.tcl`.

---

## Concept 2 — Case and trim

```tcl
string tolower "Hi"
string toupper "Hi"
string totitle "hello world"
string trim "  x  "
```

See `03_case.tcl`, `04_trim.tcl`.

---

## Concept 3 — Find and compare

```tcl
string first a banana     ;# 1
string last  a banana     ;# 5
string match ban* banana  ;# 1
string equal a a          ;# 1
string compare a b        ;# -1
```

`-1` from `first`/`last` means “not found”.

See `05_find_match.tcl`.

---

## Concept 4 — Map, replace, repeat, reverse, cat

```tcl
string map {cats dogs} "I like cats"
string replace $s 2 3 XX
string repeat "* " 3
string reverse abc
string cat Hello { } World
```

See `06_map_replace.tcl`, `07_repeat_reverse_cat.tcl`.

---

## Concept 5 — `string is` and discovery

```tcl
string is integer -strict 42
# list all subcommands:
dict keys [namespace ensemble configure string -map]
```

See `08_string_is.tcl`, `09_word_byte.tcl`, `11_discover_subcommands.tcl`.

---

## Daily practice

| Day | Goal | Files |
|-----|------|-------|
| 1 | length / index / range | `01`, `02` |
| 2 | case / trim | `03`, `04` |
| 3 | find / match | `05` |
| 4 | map / replace / repeat | `06`, `07` |
| 5 | **string_toolkit** | `10` |

### Checklist

- [ ] length / index / range  
- [ ] case + trim  
- [ ] first / match / equal  
- [ ] map / replace  
- [ ] toolkit report written  

---

## Common mistakes

| Symptom | Fix |
|---------|-----|
| `first` returns `-1` | Substring missing — check spelling/case |
| `match` always 0 | Need glob-style `*` / `?`, not regex (regex = Week 22) |
| Trim did nothing | Characters to trim are not spaces — pass the char set |

---

## Example scripts

```bash
make week6-01
make week6
make week6-10
```

| # | File | Focus |
|---|------|-------|
| 01–02 | length / index / range | Day 1 |
| 03–04 | case / trim | Day 2 |
| 05 | find / match | Day 3 |
| 06–07 | map / transform | Day 4 |
| 08–09 | `string is` / word / byte | Extra |
| 10 | **string_toolkit** | Project |
| 11–12 | discover + checklist | Wrap-up |

---

## Challenge

Write a proc `slugify s` that trims, lowercases, and maps spaces to `_`.

---

## Looking ahead

Week 7 — advanced lists (`lsearch` `lsort` `lmap` …). Still M10; Calibre waits until week 21.

---

## Parent / teacher note

M10 uses **tclsh**, not calibredrv. Success: `make week6-10` writes `tmp/week6_toolkit.txt`.
