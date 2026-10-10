# Tcl / tclsh — How to Get Help

> Companion to [PLAN.md](../PLAN.md) and [lessons/STUDY_GUIDE_zh.md](../lessons/STUDY_GUIDE_zh.md).  
> **Important:** plain `tclsh` does **not** have a `help` command. You learn by docs, error messages, and `info`.

---

## Quick commands

```bash
make help-tcl
# or
tclsh tools/show_tcl_help.tcl
```

Inside interactive `tclsh`:

```tcl
info commands          ;# all command names
info commands set*     ;# commands starting with set
info vars              ;# global variables
puts $tcl_version      ;# e.g. 8.6
exit
```

---

## Three ways to learn a Tcl command

### 1. Read the error message (best for beginners)

Tcl tells you when something is wrong:

| You type | Tcl says | Meaning |
|----------|----------|---------|
| `setx 1` | `invalid command name "setx"` | Typo — use `set` |
| `puts Hello world` | `extra characters after close-quote` | Need quotes: `puts "Hello world"` |
| `puts name` (when you wanted a variable) | prints `name` | Use `$name` to read the box |

**Practice:** run a lesson script, copy the error, search this file or STUDY_GUIDE.

### 2. Manual pages (Linux)

```bash
man 3 puts
man 3 set
man 3 expr
man 3 foreach
```

If `man 3 puts` says "No manual entry", install Tcl docs or use the online manual below.

### 3. Official Tcl 8.6 manual (online)

- [Tcl commands index](https://www.tcl-lang.org/man/tcl8.6/TclCmd/contents.htm)
- Search for command name: `puts`, `set`, `list`, `proc`, etc.

---

## `info` — Tcl’s built-in discovery tool

| Command | What it tells you |
|---------|-------------------|
| `info commands` | List available commands |
| `info commands l*` | List commands matching pattern |
| `info vars` | Global variable names |
| `info exists name` | 1 if variable `name` exists, else 0 |
| `info script` | Path of file being run |
| `info args procname` | Argument list **only for procs you defined** |
| `info body procname` | Body **only for procs you defined** |

Built-in commands like `puts` and `set` are **not** procedures — `info args puts` will fail. That is normal.

---

## Week-by-week: which commands to look up

| Week | Commands | Manual section |
|------|----------|----------------|
| 1 | `puts`, `exit` | puts |
| 2 | `set`, `expr` | set, expr |
| 3 | `list`, `lindex`, `llength`, `lappend` | list, lindex, … |
| 4 | `if`, `foreach`, `for`, `while`, `incr` | if, foreach, for, while |
| 5 | `proc`, `return`, `open`, `close`, `gets`, `file` | proc, open, file |
| 6 | `oo::class`, `oo::define` | oo::class (TclOO) |

---

## Interactive vs script file

| Mode | How to start | When to use |
|------|--------------|-------------|
| Interactive | `tclsh` then type lines | Quick experiments |
| Script | `tclsh my.tcl` or `make week1-01` | Real homework |

In interactive mode, type one command, press Enter, see result. Type `exit` to leave.

---

## Common beginner errors (full table)

| Error message | Likely cause | Fix |
|---------------|--------------|-----|
| `can't read "x": no such variable` | Used `$x` before `set x` | Add `set x ...` above |
| `wrong # args: should be "..."` | Too few/many arguments | Compare with lesson example |
| `syntax error in expression` | Bad `expr` or `if` condition | Use `{ $a + 1 }` inside expr |
| `extra characters after close-quote` | Unmatched `"` | Count quote pairs |
| `invalid command name "layout"` | Ran Calibre code in `tclsh` | Use `make week7-01` / calibredrv |

---

## See also

- [lessons/STUDY_GUIDE_en.md](../lessons/STUDY_GUIDE_en.md) — expanded explanations
- [lessons/](../lessons/) — weekly lessons with examples
