# Week 3 — A String of Candy: Lists

> Part of the [10-week Tcl learning plan](../../PLAN.md).  
> Goal this week: create lists, pick one item with `lindex`, count with `llength`, and grow lists with `lappend`.

---

## Learning goals

By the end of this week, you should be able to:

1. Build a list with `list item1 item2 item3` and store it in a variable.
2. Use `lindex $L 0` to get the first item (remember: counting starts at **0**).
3. Use `lindex $L end` or math with `llength` to get the last item.
4. Use `llength $L` to count how many items are in a list.
5. Use `lappend` to add new items to the end of a list stored in a variable.
6. Finish a class-schedule script that prints a chosen period from a list.

When you can build a list, count it, pick any item, and add new items without copying every line from the examples, Week 3 is done.

---

## Big idea (in everyday words)

Week 2 gave you **one box, one value**. Week 3 gives you **one box, many values in a row** — like candy on a string.

| Tcl idea | Everyday metaphor | What you will do this week |
|----------|-------------------|----------------------------|
| `list a b c` | Three candies threaded on one string | Build fruit lists, schedules |
| `set L [list ...]` | Put the whole string in one labeled box | Store the list in a variable |
| `lindex $L 0` | Pick the **1st** candy (index 0) | Get first color, first class |
| `lindex $L end` | Pick the **last** candy | Get last fruit, last period |
| `llength $L` | Count how many candies | "There are N kinds of fruit" |
| `lappend L new` | Tie one more candy on the end | Grow a shopping list |

You still use `set`, `$`, `puts`, and `expr` from earlier weeks. Lists are the new tool.

---

## What you need before you start

### Prerequisites

- Week 1: `puts`, scripts, comments.
- Week 2: `set`, `$variable`, `expr {$a - 1}` for index math.

### Tools

Terminal, `tclsh`, text editor — same as before.

### Quick check

```bash
make check
make week3-01
```

Expected output includes:

```text
My fruit list: apple banana cherry
```

---

## Concept 1 — `list` builds a string of items

### The shape of a list command

```tcl
set fruits [list apple banana cherry]
puts $fruits
```

| Part | Meaning |
|------|---------|
| `[list apple banana cherry]` | Build a list; `[...]` runs the command and stores the result |
| `$fruits` | The whole list as one value |
| Spaces between items | Each word is one list element (for simple lists) |

### Expected output

```text
apple banana cherry
```

Tcl prints list items separated by spaces. That is normal.

### Step-by-step: your first fruit list (Day 1)

1. Create `my_fruits.tcl` or open `01_list_fruits.tcl`.
2. Write `set fruits [list apple banana cherry]`.
3. Print with `puts "My fruit list: $fruits"`.
4. Save and run: `make week3-01`.
5. Change the fruits to your favorites; run again.

---

## Concept 2 — `lindex` picks one item (Day 2)

### Index starts at 0

| Human count | Tcl index | Item in `{apple banana cherry}` |
|-------------|-----------|----------------------------------|
| 1st | `0` | apple |
| 2nd | `1` | banana |
| 3rd | `2` | cherry |

This surprises many beginners. **First item = index 0.**

### Pick first and second

```tcl
set colors [list red green blue]
set first [lindex $colors 0]
set second [lindex $colors 1]
puts "First: $first"
puts "Second: $second"
```

Output:

```text
First: red
Second: green
```

### Pick the last item

Easy way:

```tcl
set last [lindex $fruits end]
```

Math way (helps you understand):

```tcl
set n [llength $fruits]
set lastIndex [expr {$n - 1}]
set last [lindex $fruits $lastIndex]
```

Both get the last fruit. See `04_lindex_last.tcl`.

---

## Concept 3 — `llength` counts items (Day 3)

```tcl
set fruits [list apple banana cherry orange grape]
set n [llength $fruits]
puts "There are $n kinds of fruit on my list."
```

Output:

```text
There are 5 kinds of fruit on my list.
```

Use `llength` whenever you need "how many?" — before a loop (Week 4) or to find the last index.

---

## Concept 4 — `lappend` adds to the end (Day 4)

```tcl
set fruits [list apple banana cherry]
lappend fruits orange
lappend fruits grape
puts $fruits
```

Output:

```text
apple banana cherry orange grape
```

Rules:

1. First argument is the **variable name** (no `$`): `lappend fruits orange`.
2. Each `lappend` adds **one** new item at the end.
3. The variable `fruits` is updated in place — you do not need `set` again.

---

## Concept 5 — Print every item by hand (before loops)

Week 4 will teach `foreach`. For now you can print each item with `lindex`:

```tcl
set pets [list cat dog rabbit hamster]
puts "1. [lindex $pets 0]"
puts "2. [lindex $pets 1]"
puts "3. [lindex $pets 2]"
puts "4. [lindex $pets 3]"
```

See `07_print_each_manual.tcl`. Repetitive? Yes — that is why loops come next week.

---

## Daily practice (≈30–45 minutes each day)

| Day | Goal | What to do in detail | Suggested file |
|-----|------|----------------------|----------------|
| Day 1 | Build lists | Create fruit list; store and print | `01_list_fruits.tcl`, `02_store_and_print_list.tcl` |
| Day 2 | `lindex` | Print 1st, 2nd, and last item | `03_lindex_first.tcl`, `04_lindex_last.tcl` |
| Day 3 | `llength` | Print "There are N kinds of fruit" | `05_llength_count.tcl`, `08_fruit_count_message.tcl` |
| Day 4 | `lappend` | Add two new fruits to a list | `06_lappend_add.tcl`, `09_growing_shopping_list.tcl` |
| Day 5 | **Week project** | Class schedule + print one period | `10_today_schedule.tcl` |

Bonus: `07_print_each_manual.tcl`, `11_list_of_lists.tcl`, `12_run_checklist.tcl`.

### Week checklist

- [ ] I can create a list with `list`.
- [ ] I remember that index **0** is the first item.
- [ ] I can use `lindex` to pick any item.
- [ ] I can use `lindex ... end` for the last item.
- [ ] I can use `llength` to count items.
- [ ] I can use `lappend` to add items.
- [ ] I finished my class schedule project.

---

## Common mistakes (and fixes)

| What you see / do | What it usually means | Fix |
|-------------------|----------------------|-----|
| `lindex $fruits 1` when you wanted first | Off-by-one: human 1st ≠ index 1 | First item is index **0** |
| `lindex fruits 0` | Forgot `$` when reading variable | Use `lindex $fruits 0` |
| `lappend $fruits x` | Put `$` on variable name in lappend | Write `lappend fruits x` |
| Empty or wrong last item | Used wrong index | Try `lindex $L end` |
| `list [list a b] c` confusion | Nested lists (bonus topic) | Stick to flat lists until `11_list_of_lists.tcl` |

---

## Example scripts in this folder (full list)

From the project root:

```bash
make week3-01
make week3
make list WEEK=3
make run WEEK=3 EX=10
```

Or:

```bash
tclsh lessons/3/01_list_fruits.tcl
tclsh lessons/3/02_store_and_print_list.tcl
tclsh lessons/3/03_lindex_first.tcl
tclsh lessons/3/04_lindex_last.tcl
tclsh lessons/3/05_llength_count.tcl
tclsh lessons/3/06_lappend_add.tcl
tclsh lessons/3/07_print_each_manual.tcl
tclsh lessons/3/08_fruit_count_message.tcl
tclsh lessons/3/09_growing_shopping_list.tcl
tclsh lessons/3/10_today_schedule.tcl
tclsh lessons/3/11_list_of_lists.tcl
tclsh lessons/3/12_run_checklist.tcl
```

| # | File | What you practice | What success looks like |
|---|------|-------------------|-------------------------|
| 01 | `01_list_fruits.tcl` | First `list` | Fruit names print |
| 02 | `02_store_and_print_list.tcl` | Store + early `lindex` | List and first items |
| 03 | `03_lindex_first.tcl` | Index 0 and 1 | First and second colors |
| 04 | `04_lindex_last.tcl` | Last item two ways | Last fruit correct |
| 05 | `05_llength_count.tcl` | Count items | "N kinds of fruit" |
| 06 | `06_lappend_add.tcl` | Add two items | Longer list after lappend |
| 07 | `07_print_each_manual.tcl` | Print all by hand | Four pets listed |
| 08 | `08_fruit_count_message.tcl` | Count + first/last | Inventory card |
| 09 | `09_growing_shopping_list.tcl` | Growing list | Start 2 items, end 5 |
| 10 | `10_today_schedule.tcl` | **Week project** | Full schedule + highlight |
| 11 | `11_list_of_lists.tcl` | Bonus nested list | Table rows |
| 12 | `12_run_checklist.tcl` | Week 3 checklist | Boxes print correctly |

---

## Challenge (optional, full requirements)

Customize `10_today_schedule.tcl` so it includes:

1. Your real weekday name  
2. At least **six** class subjects in the list  
3. A variable `period` (1–6) for which class to highlight  
4. Correct subject for that period using `lindex` and `expr {$period - 1}`  
5. A line: `Total: N periods` using `llength`  
6. Use `lappend` once to add a bonus class after the list is created  
7. At least four `#` comments and a border with `=`  

---

## Looking ahead

**Week 4** introduces **conditions and loops**:

- `if {score >= 60} { puts "Pass" }` — decide what to do.
- `foreach item $list { puts $item }` — visit every list item without writing `lindex` five times.
- `for` and `while` — repeat actions.

Lists hold the data; loops will help you **walk through** them automatically.

---

## Parent / teacher note

- Still plain `tclsh`; no Calibre.
- Drill **index 0 = first** until it sticks; draw a number line 0..n-1.
- `lappend` vs `set`: first arg is bare name, like `set`.
- Success: child changes subjects in `10_today_schedule.tcl`, sets `period` to 4, runs `make week3-10`, and explains why we use `expr {$period - 1}` for `lindex`.
