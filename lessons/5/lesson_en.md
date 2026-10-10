# Week 5 — Little Helpers: Procedures and Files

> Part of the [10-week Tcl learning plan](../../PLAN.md).  
> Goal this week: train reusable **procedures (`proc`)** and read/write simple **text files**.

---

## Learning goals

By the end of this week, you should be able to:

1. Define a procedure: `proc greet {name} { puts "Hi $name!" }` and call it.
2. Use `return` to send a result back from a proc (for example, `add`).
3. Open a file for writing, write lines with `puts $channel ...`, and `close` it.
4. Open a file for reading and read lines with `gets` in a `while` loop.
5. Use `file mkdir` and `file join` for folders and paths.
6. Finish a **toolbox** script with at least three procs plus file logging.

When you can combine variables, lists, `if`, loops, at least one `proc`, and file read/write in one script, Week 5 is done.

---

## Big idea (in everyday words)

| Tcl idea | Everyday metaphor | What you will do this week |
|----------|-------------------|----------------------------|
| `proc greet {...}` | Train a small dog to greet on command | Reuse code without retyping |
| `return` | Dog brings back a ball | `add` returns a number |
| `open` / `close` | Open notebook, write, close notebook | Diary in `tmp/` |
| `gets` | Read one line from the page | Print file line by line |
| `file join` | Glue path pieces safely | Build `tmp/notes.txt` |

**Bridge to OOP:** A `proc` is an action without an owner. Next week, **objects** own their methods — like each pet knowing its own `speak`.

---

## What you need before you start

### Prerequisites

- Weeks 1–4: `puts`, variables, lists, `if`, loops.

### Tools

- `tclsh`, text editor, terminal.
- Writable `tmp/` folder under the project root (examples create it with `file mkdir tmp`).

### Run from project root

File paths in examples use `tmp/...` relative to the **project root** (where `make` runs):

```bash
make week5-05
make week5-07
```

---

## Concept 1 — `proc` defines a reusable helper (Day 1)

```tcl
proc greet {name} {
    puts "Hi $name!"
}

greet "Amy"
greet "Bob"
```

| Part | Meaning |
|------|---------|
| `proc` | Define a procedure |
| `greet` | Name of the helper |
| `{name}` | Parameter list (one argument) |
| `{ puts ... }` | Body — commands to run |

Call it like a command: `greet "Amy"`.

---

## Concept 2 — `return` sends back a value (Day 2)

```tcl
proc add {a b} {
    return [expr {$a + $b}]
}

set sum [add 15 4]
puts $sum
```

Output: `19`

Use `return` when the proc **computes** something callers need later.

---

## Concept 3 — Write a text file (Day 3)

```tcl
file mkdir tmp

set path tmp/week5_diary.txt
set fh [open $path w]

puts $fh "Line 1"
puts $fh "Line 2"

close $fh
```

| Step | Command | Notes |
|------|---------|-------|
| Ensure folder | `file mkdir tmp` | Safe if folder exists |
| Open for write | `open $path w` | `w` = write (creates/overwrites) |
| Write | `puts $fh "text"` | Note `$fh` — not stdout |
| Close | `close $fh` | Always close when done |

---

## Concept 4 — Read a text file (Day 4)

```tcl
set fh [open $path r]

while {[gets $fh line] >= 0} {
    puts $line
}

close $fh
```

`gets $fh line` reads one line into `line`. It returns `-1` at end-of-file — loop stops.

---

## Concept 5 — Paths: `file join` and checks (Day 3–4)

```tcl
set path [file join tmp week5_notes.txt]
```

`file join` builds paths correctly on different operating systems.

```tcl
if {[file exists $path]} {
    puts "Found: $path"
}
```

See `09_file_exists_size.tcl`.

---

## Concept 6 — Toolbox project (Day 5)

`10_toolbox.tcl` combines:

- `greet` — returns a string  
- `add` — returns a sum  
- `printList` — prints a list with `foreach`  
- `appendLog` — appends lines to a log file  

Then reads the log back and prints it.

---

## Daily practice

| Day | Goal | Files |
|-----|------|-------|
| Day 1 | `proc greet` | `01_proc_greet.tcl`, `02_proc_greet_many.tcl` |
| Day 2 | `return`, proc + `if` | `03_proc_add_return.tcl`, `04_proc_pass_fail.tcl` |
| Day 3 | Write files | `05_write_diary.tcl`, `06_write_with_file_join.tcl` |
| Day 4 | Read files | `07_read_diary.tcl`, `08_read_line_by_line.tcl` |
| Day 5 | **Toolbox** | `10_toolbox.tcl` |

Bonus: `09_file_exists_size.tcl`, `11_proc_double.tcl`, `12_run_checklist.tcl`.

### Week checklist

- [ ] I can define and call a `proc`.
- [ ] I can use `return`.
- [ ] I can write a text file and close it.
- [ ] I can read a file with `gets`.
- [ ] I can use `file join` / `file mkdir`.
- [ ] I finished the toolbox project.

---

## Common mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `can't read "fh"` | Used `$fh` before `open` | `set fh [open $path w]` first |
| Empty output file | Wrote to stdout not file | Use `puts $fh`, not bare `puts` |
| `couldn't open` | Wrong path or no `tmp/` | Run from project root; `file mkdir tmp` |
| Forgot `close` | File left open | Always `close $fh` |
| Proc body uses wrong args | Parameter name typo | Match `{name}` and `$name` |

---

## Example scripts

```bash
make week5-01
make week5
make list WEEK=5
```

| # | File | Practice |
|---|------|----------|
| 01 | `01_proc_greet.tcl` | First proc |
| 02 | `02_proc_greet_many.tcl` | proc + foreach |
| 03 | `03_proc_add_return.tcl` | return |
| 04 | `04_proc_pass_fail.tcl` | proc + if |
| 05 | `05_write_diary.tcl` | write diary |
| 06 | `06_write_with_file_join.tcl` | file join |
| 07 | `07_read_diary.tcl` | read diary |
| 08 | `08_read_line_by_line.tcl` | gets + while |
| 09 | `09_file_exists_size.tcl` | file exists/size |
| 10 | `10_toolbox.tcl` | **Week project** |
| 11 | `11_proc_double.tcl` | proc calls proc |
| 12 | `12_run_checklist.tcl` | Checklist |

---

## Challenge

Extend `10_toolbox.tcl`:

1. Add proc `subtract {a b}` with `return`  
2. Add proc `writeReport {path scores}` that writes each score to a file  
3. Use `if` inside a proc to label Pass/Fail per score  
4. Read the report back and print with line numbers  
5. Four `#` comments explaining each proc  

---

## Looking ahead

**Week 6 — TclOO:** classes, objects, methods.  
Think: many pets each with their own `speak` — that is OOP. Procs this week are **global helpers**; methods next week belong to **objects**.

---

## Parent / teacher note

- Run `make week5` from project root so `tmp/` paths resolve.
- `tmp/week5_*.txt` files are created by examples; safe to delete between runs.
- Success: child explains difference between `puts "hi"` and `puts $fh "hi"`.
