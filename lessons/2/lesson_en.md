# Week 2 — Boxes with Labels: Variables and Strings

> Part of the [10-week Tcl learning plan](../../PLAN.md).  
> Goal this week: store values with `set`, read them with `$`, and do simple math with `expr`.

---

## Learning goals

By the end of this week, you should be able to:

1. Use `set` to put a value into a named variable (a labeled box).
2. Use `$variableName` to read a value and print it with `puts`.
3. Build sentences inside double quotes where `$name` is replaced by the stored value.
4. Change a variable by calling `set` again with the same name.
5. Use `expr {$a + $b}` and `expr {$age + 1}` for simple addition and subtraction.
6. Finish a report-card script that stores three scores and prints a total.

When you can write a short self-introduction using variables (not copying every word from the examples), Week 2 is done.

---

## Big idea (in everyday words)

Last week you printed **fixed text** — every word was typed directly into `puts`. This week you learn **variables**: labeled boxes that hold values. Change what is inside the box, and every `$label` that reads from it shows the new value.

| Tcl idea | Everyday metaphor | What you will do this week |
|----------|-------------------|----------------------------|
| `set name "Amy"` | Put `"Amy"` in a box labeled `name` | Store names, scores, ages |
| `$name` | Open the box labeled `name` | Use the value in `puts` or `expr` |
| `"Hello, $name"` | Say a sentence but swap in the box contents | Build messages from parts |
| `expr {$a + $b}` | Use a calculator for numbers in boxes | Add scores, age + 1 |
| `{...}` braces | A sealed bag — nothing inside is substituted | Print `$name` literally when teaching |

You still use `puts` and `.tcl` files from Week 1. You are adding **memory** to your scripts.

---

## What you need before you start

### Prerequisites from Week 1

- You can run `tclsh` and run a `.tcl` file.
- You know `puts` and `#` comments.
- You can read script output and fix simple quote errors.

### Tools

Same as Week 1: terminal, `tclsh`, text editor.

### Check Tcl still works

```bash
make check
```

Or:

```bash
tclsh lessons/2/01_set_one_variable.tcl
```

Expected output:

```text
Amy
```

### Run Week 2 examples with Make

From the project root:

```bash
make week2-01
make week2
make list WEEK=2
```

---

## Concept 1 — `set` stores a value in a labeled box

### The shape of a set command

```tcl
set name "Amy"
```

| Part | Example | Meaning |
|------|---------|---------|
| Command | `set` | Store a value |
| Variable name | `name` | The label on the box (no `$` here) |
| Value | `"Amy"` | What goes inside |

### Rules to remember

1. **Creating** a variable: `set variableName value` — no `$` on the name in `set`.
2. Variable names are usually one word: `name`, `school`, `mathScore`. No spaces in the name.
3. Text values use quotes: `set name "Amy"`.
4. Number values can omit quotes: `set age 10` (both work; `set age "10"` is also OK for now).

### First complete example

```tcl
set name "Amy"
puts $name
```

Expected output:

```text
Amy
```

Notice: `puts $name` uses `$` because you are **reading** the box, not labeling it.

### Step-by-step: three variables (Day 1)

1. Open `02_three_variables.tcl` or create your own file.
2. Add three `set` lines for name, school, and grade.
3. Add three `puts` lines that print each variable.
4. Save and run: `make week2-02`
5. Change the three values to your own facts; run again and confirm the output changed.

---

## Concept 2 — `$` reads a variable

### When to use `$`

| Situation | Write | Example |
|-----------|-------|---------|
| Store a value | `set name "Amy"` | No `$` on `name` |
| Read a value alone | `puts $name` | `$` before `name` |
| Read inside a string | `puts "Hi, $name!"` | `$` inside `"..."` |

### Wrong vs right

```tcl
set name "Amy"
puts name      ;# WRONG for beginners — prints the word "name", not Amy
puts $name     ;# RIGHT — prints Amy
```

### Building one sentence from two variables (Day 2)

```tcl
set name "Amy"
set city "Shanghai"
puts "Hello, my name is $name and I live in $city."
```

Expected output:

```text
Hello, my name is Amy and I live in Shanghai.
```

Tcl replaces `$name` and `$city` **before** printing. You write the template once; the boxes supply the facts.

---

## Concept 3 — Change a variable with `set` again (Day 3)

A variable is not locked forever. The same label can hold a new value:

```tcl
set favoriteColor "blue"
puts "Before: $favoriteColor"

set favoriteColor "green"
puts "After : $favoriteColor"
```

Expected output:

```text
Before: blue
After : green
```

The label `favoriteColor` stayed the same; only the contents changed. Any later `$favoriteColor` uses the **latest** value.

### Why this matters

You will use this when:

- Updating a score after a quiz.
- Simulating “next year” age.
- Fixing a typo without renaming the whole variable.

---

## Concept 4 — `expr` for simple math (Day 4)

### Why not `puts $a + $b`?

`puts` prints text. To **add numbers**, use `expr`:

```tcl
set a 15
set b 4
set sum [expr {$a + $b}]
puts "a + b = $sum"
```

Expected output:

```text
a + b = 19
```

### Parts of the pattern

| Part | Meaning |
|------|---------|
| `[expr {...}]` | Run the math and return the result |
| `{...}` inside expr | Keeps the math expression safe (good habit) |
| `$a`, `$b` inside expr | Read numbers from variables |

### Age + 1 (from PLAN)

```tcl
set age 10
set nextAge [expr {$age + 1}]
puts "Next year I will be $nextAge."
```

Output:

```text
Next year I will be 11.
```

### Subtraction works the same way

```tcl
set apples 7
set eaten 2
set left [expr {$apples - $eaten}]
puts "Apples left: $left"
```

See `09_simple_math.tcl` for a full script.

---

## Concept 5 — Double quotes vs curly braces

### Double quotes `"..."` — substitution ON

```tcl
set name "Amy"
puts "Hello, $name!"
```

Prints: `Hello, Amy!`

### Curly braces `{...}` — substitution OFF

```tcl
set name "Amy"
puts {Hello, $name!}
```

Prints: `Hello, $name!` (literally shows `$name`)

Use braces when you want to **show** Tcl syntax in output, or when special characters should not be interpreted. Week 2: know both exist; use quotes for most messages.

---

## Daily practice (≈30–45 minutes each day)

| Day | Goal | What to do in detail | Suggested file |
|-----|------|----------------------|----------------|
| Day 1 | First `set` | Store name, school, grade; print each with `$` | `01_set_one_variable.tcl`, `02_three_variables.tcl` |
| Day 2 | Sentences with `$` | Combine two or more variables in one `puts "..."` | `03_print_with_dollar.tcl`, `06_two_strings_join.tcl` |
| Day 3 | Change values | `set` the same name twice; print before and after | `04_change_value.tcl` |
| Day 4 | Math with `expr` | Age + 1; add and subtract two numbers | `05_expr_add_one.tcl`, `09_simple_math.tcl` |
| Day 5 | **Week project** | Report card: three subjects + total score | `10_report_card.tcl` |

Extra: `07_numbers_and_strings.tcl`, `08_braces_literal.tcl`, `11_intro_with_variables.tcl`, `12_run_checklist.tcl`.

### Week checklist

- [ ] I can use `set` to store text and numbers.
- [ ] I know when to write `name` vs `$name`.
- [ ] I can print variables inside double-quoted strings.
- [ ] I can change a variable and see new output.
- [ ] I can use `expr` for + and −.
- [ ] I finished my report card with a correct total.

---

## Common mistakes (and fixes)

| What you see / do | What it usually means | Fix |
|-------------------|----------------------|-----|
| `can't read "name": no such variable` | Used `$name` before `set name ...` | Add `set name "..."` above the `puts` |
| Output shows `name` instead of Amy | Wrote `puts name` without `$` | Use `puts $name` |
| `syntax error in expression` | Bad `expr` syntax | Use `expr {$a + $b}` with spaces around `+` or `−` |
| `"8" + "3"` gives wrong result | Treated numbers as plain text in wrong place | Store numbers without quotes; use `expr` for math |
| `set $name "Amy"` | Put `$` on the left side of `set` | Write `set name "Amy"` only |
| Math looks like `88 + 92 + 85` as text | Used quotes inside expr wrongly | Use `expr {$math + $english + $science}` |

---

## Example scripts in this folder (full list)

Easiest way (from the project root):

```bash
make week2-01
make week2
make list WEEK=2
make run WEEK=2 EX=10
```

Or with `tclsh`:

```bash
tclsh lessons/2/01_set_one_variable.tcl
tclsh lessons/2/02_three_variables.tcl
tclsh lessons/2/03_print_with_dollar.tcl
tclsh lessons/2/04_change_value.tcl
tclsh lessons/2/05_expr_add_one.tcl
tclsh lessons/2/06_two_strings_join.tcl
tclsh lessons/2/07_numbers_and_strings.tcl
tclsh lessons/2/08_braces_literal.tcl
tclsh lessons/2/09_simple_math.tcl
tclsh lessons/2/10_report_card.tcl
tclsh lessons/2/11_intro_with_variables.tcl
tclsh lessons/2/12_run_checklist.tcl
```

| # | File | What you practice | What success looks like |
|---|------|-------------------|-------------------------|
| 01 | `01_set_one_variable.tcl` | First `set` and `$` | Prints `Amy` (or your name) |
| 02 | `02_three_variables.tcl` | Three labeled boxes | Name, school, grade lines |
| 03 | `03_print_with_dollar.tcl` | `$` inside `"..."` | Full sentences with names |
| 04 | `04_change_value.tcl` | Re-set a variable | Before/after lines differ |
| 05 | `05_expr_add_one.tcl` | `expr {$age + 1}` | Next age prints correctly |
| 06 | `06_two_strings_join.tcl` | Join parts in one line | One sentence from two vars |
| 07 | `07_numbers_and_strings.tcl` | Text vs number boxes | Score + bonus uses expr |
| 08 | `08_braces_literal.tcl` | `{...}` no substitution | Literal `$name` in output |
| 09 | `09_simple_math.tcl` | Add and subtract | Sum and difference correct |
| 10 | `10_report_card.tcl` | **Week project** | Three scores + total |
| 11 | `11_intro_with_variables.tcl` | Bonus intro card | All fields from variables |
| 12 | `12_run_checklist.tcl` | Week 2 checklist | Checkboxes print with `{...}` |

---

## Challenge (optional, full requirements)

Rewrite `10_report_card.tcl` (or copy to `my_report_card.tcl`) so it includes:

1. Your real name and school  
2. Three subject names you choose (not only Math / English / Science)  
3. A score variable for each subject  
4. Total computed with one `expr` (not hand-typed)  
5. A line showing average: `expr {$total / 3}` (integer division is OK for now)  
6. At least four `#` comments for header, scores, total, and footer  
7. A border made with `=` characters  

---

## Looking ahead

**Week 3** introduces **lists**: a string of items like `{apple banana cherry}`.

- `list a b c` builds a list.
- `lindex $L 0` picks the first item (counting from 0).
- `llength $L` counts how many items.

Variables hold **one** value per box. Lists hold **many** values in one labeled box — like a whole string of candy on one stick.

---

## Parent / teacher note

- Still plain `tclsh` only; no Calibre required.
- Common learner confusion: `$` on read but not on write. Drill `set name` vs `$name` until automatic.
- For `expr`, accept integer division in the challenge; `double()` comes later if needed.
- Success: learner edits `set` lines in `10_report_card.tcl`, saves, runs `make week2-10`, and explains one `$` and one `expr`.
