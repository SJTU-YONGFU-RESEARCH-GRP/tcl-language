# Calibre DESIGNrev (calibredrv) — How to Get Help

> Companion to [PLAN.md](../PLAN.md). Run all examples via `./scripts/run_calibre_tcl.sh`.  
> Calibredrv **does not** use `man layout`. It teaches you through **Usage:** lines when arguments are missing.

---

## Quick commands

```bash
make help-calibre
# or
./scripts/run_calibre_tcl.sh tools/show_calibre_help.tcl
```

CLI help:

```bash
source scripts/setup_calibredrv.sh
calibredrv -h
```

---

## The #1 trick: call a command with too few arguments

Calibredrv prints **Usage:** messages. Examples captured from this machine:

### Global `layout` command

```
layout [all | copy | copy2 | create | delete | droasis | filemerge |
        filtershapes | merge | overlays | peek | tbmode] ?args ...?
```

| Subcommand | Usage (summary) |
|------------|-----------------|
| `layout create` | No args → creates empty layout, returns handle (e.g. `layout0`) |
| `layout create $file` | Open GDS/OASIS file |
| `layout peek $file` | Peek without full load |
| `layout filemerge` | Merge layouts (advanced) |

### Layout object `$L` (handle)

Wrong: `$L` alone →  
`wrong # args: should be "layout0 option ?args ... ? "`

Wrong: `$L create` alone →  
`Usage: layout0 create <layer|cell|polygon|wire|ref|text|clip>`

### `$L create` subcommands (Week 7–10)

| Kind | Usage line |
|------|------------|
| **cell** | `create cell name ?handle name?` |
| **layer** | `create layer <L> [<layer options>]` |
| **polygon** | `create polygon: cell L_D ... x1 y1 ... xn yn` |
| **wire** | `create wire: cell L_D width ... coords` |
| **text** | `create text cell L x y text ...` |
| **ref** | `create ref <incell> <refcell> <x> <y> <mirror> <angle> <mag> ...` |

### `$L` export & query

| Command | Usage hint |
|---------|------------|
| `gdsout` | `gdsout fileName[.gz] [cellName] [many options]` |
| `exists` | `exists cell <cell> \| layer <L>` |
| `bbox` | `bbox cellName` |
| `iterator` | needs more arguments (see manual) |

Run `make help-calibre` to refresh these on your machine.

---

## Interactive experiments (calibredrv -shell)

```bash
source scripts/setup_calibredrv.sh
calibredrv -shell
```

Then type:

```tcl
layout                    ;# see subcommand list (error message)
set L [layout create]
$L create                  ;# see create types
$L gdsout                  ;# see gdsout options
exit
```

---

## Official manual (authoritative)

Paths in [PLAN.md](../PLAN.md):

- **calbr_drv_ref** — Layout Commands, Layout Object
- Search HTML TOC for: `layout create`, `create polygon`, `gdsout`, `layout peek`

When Usage lines are not enough, open the manual section for the full option list.

---

## OOP connection (Week 6 → Week 7)

| Week 6 TclOO | Week 7 Calibre |
|--------------|----------------|
| `[Pet new "Mimi"]` | `[layout create]` |
| `$cat speak` | `$L create cell TOP` |
| object handle in `$cat` | layout handle in `$L` |

---

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `invalid command name "layout"` | Used `tclsh` not calibredrv | `./scripts/run_calibre_tcl.sh` |
| `couldn't open "...gds"` | File path wrong | Run from project root; check `tmp/` |
| Wrong layer format | Mixed `1`, `1.0`, `1_0` | Pick one style; see Week 8 lesson |
| Coords as one list | `create polygon` wants flat numbers | Use `eval $L create polygon ... $coords` |

---

## See also

- [examples/create_box.tcl](../examples/create_box.tcl)
- [examples/script.tcl](../examples/script.tcl) — polygon from argv + eval
- [lessons/7/](../lessons/7/) — handles week
- [lessons/STUDY_GUIDE_zh.md](../lessons/STUDY_GUIDE_zh.md) — expanded walkthrough
