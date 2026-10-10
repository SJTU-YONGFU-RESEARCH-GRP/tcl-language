# Week 1 — The Computer Can Talk: `puts` and Script Files

> Part of the [10-week Tcl learning plan](../../PLAN.md).  
> Goal this week: make the computer print text for you, and understand what a `.tcl` file is.

---

## Learning goals

By the end of this week, you should be able to:

1. Run Tcl with `tclsh`.
2. Use `puts` to print one or more lines of text.
3. Save commands in a `.tcl` script file and run it.
4. Write `#` comments so future-you remembers what each line does.
5. Finish a small “self-introduction card” script on your own.

---

## Big idea (in everyday words)

A computer is like a helpful robot. It does **exactly** what you write — no more, no less.

| Tcl idea | Everyday metaphor |
|----------|-------------------|
| Script `.tcl` | A **to-do list** for the robot |
| `puts` | “Please **say this out loud** (print it)” |
| `#` comment | A sticky note for humans; the robot **ignores** it |
| `tclsh my.tcl` | “Robot, please **follow this list**” |

You do **not** need variables, loops, or Calibre yet. This week is only about speaking.

---

## What you need

- A terminal (command line).
- Tcl installed so this works:

```bash
tclsh
```

Inside `tclsh`, try:

```tcl
puts "Hello, I am learning Tcl!"
```

Then leave with:

```tcl
exit
```

Or run a file in one shot:

```bash
tclsh lessons/1/01_hello.tcl
```

> Tip: from the project root (`tcl-language`), use the paths above. If you `cd` into `lessons/1`, then run `tclsh 01_hello.tcl`.

---

## Concept 1 — `puts` means “print this”

`puts` is short for **put string** (put text onto the screen).

```tcl
puts "Hello"
```

Rules to remember:

1. Write `puts`, then a space, then the text.
2. Put text inside **double quotes** `"..."` when it has spaces.
3. Each `puts` usually prints **one line**, then moves to the next line.

### Try it

```tcl
puts "Hello, I am learning Tcl!"
puts "My name is Amy."
puts "I like the color blue."
```

---

## Concept 2 — A `.tcl` file is a script

Typing in `tclsh` is fine for tiny tests. Real learning means saving a **script**:

1. Create a file ending in `.tcl` (example: `my_first.tcl`).
2. Put Tcl commands inside, one per line (usually).
3. Run it: `tclsh my_first.tcl`.

The computer reads the file **from top to bottom**, like reading a shopping list.

### Minimal script

```tcl
# my_first.tcl — my first Tcl script
puts "Line 1"
puts "Line 2"
puts "Line 3"
```

---

## Concept 3 — `#` comments are notes for you

Anything after `#` on a line is a **comment**. Tcl skips it.

```tcl
# This line is only for me to read
puts "The computer still prints this"   ;# end-of-line comment also works
```

Good comments answer: *What is this line doing?* Bad comments only repeat the code.

| Better | Weaker |
|--------|--------|
| `# Print my favorite color` | `# puts` |
| `# Title of the intro card` | `# line 1` |

---

## Concept 4 — Quotes and spaces (just enough for Week 1)

- `"Hello world"` — text with a space; use quotes.
- `puts Hello` — works for a **single** word with no spaces.
- Prefer quotes for beginners: always `"like this"`.

Later weeks will teach `{...}` braces and variables. Skip them for now unless an example uses them.

---

## Daily practice (≈30–45 minutes)

| Day | Task | Suggested file |
|-----|------|----------------|
| Day 1 | Confirm `tclsh` works; print `Hello, I am learning Tcl!` | `01_hello.tcl` |
| Day 2 | Print your name, age, and favorite color (one line each) | `02_about_me.tcl` |
| Day 3 | Write a script with **5** `puts` lines; run with `tclsh` | `03_five_lines.tcl` |
| Day 4 | Add `#` comments explaining every line | `04_with_comments.tcl` |
| Day 5 | **Mini project:** print a self-introduction card | `10_self_intro_card.tcl` |

### Week checklist

- [ ] I can open a terminal and run `tclsh`.
- [ ] I can print text with `puts`.
- [ ] I can create a `.tcl` file and run it.
- [ ] I can add useful `#` comments.
- [ ] I finished the self-introduction card by myself.

---

## Common mistakes (and fixes)

| What you see / do | What it usually means | Fix |
|-------------------|----------------------|-----|
| `command not found: tclsh` | Tcl not installed or not on PATH | Ask an adult to install Tcl; retry `tclsh` |
| `extra characters after close-quote` | Missing or mismatched `"` | Count quotes; keep one pair per string |
| Nothing seems to happen | You started `tclsh` but did not type `puts` | Type a `puts` line, or run a `.tcl` file |
| Chinese / special characters look wrong | Terminal encoding issue | Use UTF-8 terminal; keep text simple if needed |
| Script runs wrong file | Wrong folder | `cd` to the folder that contains the `.tcl` file |

---

## Example scripts in this folder

Run any example from the project root:

```bash
tclsh lessons/1/01_hello.tcl
tclsh lessons/1/02_about_me.tcl
# ... through 10 (and bonus 11–12)
```

| # | File | What you practice |
|---|------|-------------------|
| 01 | `01_hello.tcl` | First `puts` |
| 02 | `02_about_me.tcl` | Several lines about you |
| 03 | `03_five_lines.tcl` | A longer script |
| 04 | `04_with_comments.tcl` | `#` comments |
| 05 | `05_blank_lines.tcl` | Blank lines for readability |
| 06 | `06_ascii_art.tcl` | Fun shapes with text |
| 07 | `07_shopping_list.tcl` | A printable list |
| 08 | `08_story_three_lines.tcl` | A tiny story |
| 09 | `09_menu_card.tcl` | A “menu” layout |
| 10 | `10_self_intro_card.tcl` | **Week project** |
| 11 | `11_puts_without_newline.tcl` | `puts -nonewline` (bonus) |
| 12 | `12_run_checklist.tcl` | End-of-week checklist printout |

---

## Challenge (optional)

Change `10_self_intro_card.tcl` so it includes:

1. Your real name  
2. Your school or city  
3. One thing you want to learn in Tcl  
4. A border made of `=` or `*` characters  

Do **not** use variables yet unless you already peeked at Week 2 — plain `puts` is enough.

---

## Looking ahead

**Week 2** introduces **variables**: boxes with labels (`set name "Amy"`, then `$name`).  
This week you only **print fixed text**. Next week the text can change.

---

## Parent / teacher note

- Environment for Calibre (`calibredrv`) is **not** required this week.
- Success looks like: child can edit a `.tcl` file, save it, run `tclsh`, and explain one comment.
- If stuck, run the numbered examples in order; then ask the child to copy `10_self_intro_card.tcl` and change the words.
