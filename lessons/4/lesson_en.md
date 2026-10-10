# Week 4 — If…Then…: Conditions and Loops

> Part of the [10-week Tcl learning plan](../../PLAN.md).  
> Goal this week: make programs that **decide** (`if`) and **repeat** (`foreach`, `for`, `while`).

---

## Learning goals

By the end of this week, you should be able to:

1. Write `if {condition} { ... } else { ... }` to choose between actions.
2. Use `foreach item $list { ... }` to visit every item in a list.
3. Use `for {set i 1} {$i <= 10} {incr i} { ... }` to count with a loop variable.
4. Use `while {condition} { ... }` to repeat until a condition becomes false.
5. Combine `if` with loops (for example, pass/fail for each score in a list).
6. Finish a guess-the-number script that compares guesses to a secret number.

When you can write a small script with at least one `if` and one loop without copying every line, Week 4 is done.

---

## Big idea (in everyday words)

So far your scripts mostly ran **straight down** — line 1, line 2, line 3. This week they learn to **branch** and **loop**.

| Tcl idea | Everyday metaphor | What you will do this week |
|----------|-------------------|----------------------------|
| `if {rain} { umbrella }` | If it rains, bring an umbrella | Pass/Fail by score |
| `foreach fruit $list` | Taste every candy on the string | Print each fruit |
| `for {set i 1} ...` | Count steps: 1, 2, 3 … 10 | Print numbers, times table |
| `while {$n > 0}` | Keep going until the job is done | Countdown 5…1, then "Launch!" |

You still use variables, lists, `puts`, and `expr` from Weeks 1–3.

---

## What you need before you start

### Prerequisites

- Week 2: `set`, `$`, `expr`.
- Week 3: `list`, `lindex`, `llength`, `lappend`.

### Tools

Terminal, `tclsh`, text editor.

### Quick check

```bash
make week4-01
```

---

## Concept 1 — `if` makes decisions (Day 1)

### Shape of an if / else

```tcl
set score 75

if {$score >= 60} {
    puts "Pass"
} else {
    puts "Fail"
}
```

### Rules to remember

1. The **condition** goes inside `{ curly braces }`: `{ $score >= 60 }`.
2. The **body** (what to do) also uses `{ ... }` blocks.
3. Comparisons: `>=`, `<=`, `==`, `!=`, `<`, `>`.
4. Use `elseif` for extra branches (see `02_if_else_messages.tcl`).

### Expected output (score 75)

```text
Pass
```

### Why braces around the condition?

Tcl should check the condition **later**, as a whole expression. `{ $score >= 60 }` is the safe beginner pattern.

---

## Concept 2 — `foreach` walks a list (Day 2)

```tcl
set fruits [list apple banana cherry]

foreach fruit $fruits {
    puts "I like $fruit."
}
```

Output:

```text
I like apple.
I like banana.
I like cherry.
```

Each time through the loop, `fruit` holds the **next** item. No manual `lindex 0`, `lindex 1`, …

### foreach + counter (optional pattern)

```tcl
set n 0
foreach color $colors {
    incr n
    puts "$n. $color"
}
```

See `05_foreach_with_index.tcl`.

---

## Concept 3 — `for` counts with a loop variable (Day 3)

```tcl
for {set i 1} {$i <= 10} {incr i} {
    puts $i
}
```

Three parts inside `for`:

| Part | Example | Role |
|------|---------|------|
| Start | `set i 1` | Create loop variable |
| Condition | `$i <= 10` | Keep looping while true |
| Step | `incr i` | Add 1 each time |

Output: numbers 1 through 10, one per line.

See `07_for_times_table.tcl` for using `expr` inside the loop body.

---

## Concept 4 — `while` repeats until done (Day 4)

```tcl
set n 5
while {$n > 0} {
    puts $n
    incr n -1
}
puts "Launch!"
```

Output:

```text
5
4
3
2
1
Launch!
```

The condition `$n > 0` is checked **before** each repetition. When `n` becomes 0, the loop stops.

**Important:** Something inside the loop must change `n` (here `incr n -1`), or the loop runs forever.

---

## Concept 5 — Guess-the-number project (Day 5)

The project combines `foreach`, `if`, `elseif`, `else`, and `break`.

Our batch-friendly version uses a **list of guesses** instead of keyboard input, so `make week4-10` always works:

```tcl
set secret 7
foreach guess $guesses {
    if {$guess == $secret} {
        puts "CORRECT!"
        break
    } elseif {$guess < $secret} {
        puts "too low"
    } else {
        puts "too high"
    }
}
```

`break` exits the loop early when the answer is found.

Later (Week 5+) you can add `gets stdin` for interactive play with a parent’s help.

---

## Daily practice (≈30–45 minutes each day)

| Day | Goal | Suggested files |
|-----|------|-----------------|
| Day 1 | Pass / Fail with `if` | `01_if_pass_fail.tcl`, `02_if_else_messages.tcl`, `03_if_check_three_scores.tcl` |
| Day 2 | `foreach` over lists | `04_foreach_fruits.tcl`, `05_foreach_with_index.tcl` |
| Day 3 | `for` 1..10 | `06_for_one_to_ten.tcl`, `07_for_times_table.tcl` |
| Day 4 | `while` countdown | `08_while_countdown.tcl`, `09_while_add_until.tcl` |
| Day 5 | **Week project** | `10_guess_number_game.tcl` |

Bonus: `11_if_foreach_combined.tcl`, `12_run_checklist.tcl`.

### Week checklist

- [ ] I can write `if / else` with a condition in braces.
- [ ] I can use `foreach` on a list.
- [ ] I can use `for` to count.
- [ ] I can use `while` until a condition fails.
- [ ] I finished the guess-number game.

---

## Common mistakes (and fixes)

| Symptom | Cause | Fix |
|---------|-------|-----|
| `syntax error in expression` | Condition not in braces | Use `if {$x >= 60} {` |
| Infinite loop in `while` | Never change the variable | Add `incr n -1` or similar |
| `foreach` prints nothing | Wrong variable or empty list | Check `set fruits [list ...]` |
| `if $score >= 60` error | Missing braces | Wrap condition: `{ $score >= 60 }` |
| Loop runs one time too many/few | Off-by-one in `for` | Check `<=` vs `<` |

---

## Example scripts (full list)

```bash
make week4-01
make week4
make list WEEK=4
```

| # | File | Practice |
|---|------|----------|
| 01 | `01_if_pass_fail.tcl` | Basic pass/fail |
| 02 | `02_if_else_messages.tcl` | elseif grades |
| 03 | `03_if_check_three_scores.tcl` | Three subjects |
| 04 | `04_foreach_fruits.tcl` | foreach basics |
| 05 | `05_foreach_with_index.tcl` | foreach + counter |
| 06 | `06_for_one_to_ten.tcl` | for 1..10 |
| 07 | `07_for_times_table.tcl` | for + expr |
| 08 | `08_while_countdown.tcl` | countdown + Launch |
| 09 | `09_while_add_until.tcl` | while until goal |
| 10 | `10_guess_number_game.tcl` | **Week project** |
| 11 | `11_if_foreach_combined.tcl` | foreach + if |
| 12 | `12_run_checklist.tcl` | Checklist |

---

## Challenge (optional)

Extend `10_guess_number_game.tcl`:

1. Secret number between 1 and 20  
2. At least 6 guesses in the list  
3. Count how many guesses were needed when correct  
4. Print "Game over" if no guess succeeds  
5. Use `while` instead of `foreach` to try guesses one by one from a list index  

---

## Looking ahead

**Week 5** introduces **procedures (`proc`)** and **file I/O**:

- `proc greet {name} { puts "Hi $name" }` — reusable helpers.
- `open`, `gets`, `puts`, `close` — read and write text files.

Your loops and `if` blocks will move **inside** procs next week.

---

## Parent / teacher note

- Conditions and loop headers almost always use `{ braces }` — drill this early.
- `10_guess_number_game.tcl` is intentionally batch-mode; interactive `gets` is optional stretch.
- Success: child modifies pass threshold or guess list, runs `make week4-10`, explains one `if` and one loop.
