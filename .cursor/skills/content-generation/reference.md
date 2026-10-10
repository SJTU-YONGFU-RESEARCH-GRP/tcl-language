# Content Generation — Reference

## PLAN.md week headings

Use these to locate source material in [PLAN.md](../../PLAN.md):

```
## 第 1 周 — 电脑会说话：`puts` 与脚本文件
## 第 2 周 — 盒子里的东西：变量与字符串
## 第 3 周 — 一串糖果：列表（list）
## 第 4 周 — 如果……就……：条件与循环
## 第 5 周 — 小帮手：过程（proc）与文件
## 第 6 周 — 会做事的小玩具：类、对象、方法（TclOO）
## 第 7 周 — 启动方式 + API-A：`layout create` 与句柄
## 第 8 周 — API-B 创建几何：cell / layer / polygon / wire / text + 写出文件
## 第 9 周 — API-A/B 查询：打开、提问、peek（不瞎改）
## 第 10 周 — API 层次：`create ref` + 多 API 毕业作品
```

English title examples (derive consistent EN titles):

| N | English title |
|---|---------------|
| 2 | Boxes with Labels: Variables and Strings |
| 3 | A String of Candy: Lists |
| 4 | If…Then…: Conditions and Loops |
| 5 | Little Helpers: Procedures and Files |
| 6 | Toys That Do Things: Classes, Objects, Methods (TclOO) |
| 7 | Getting Started + layout create and Handles |
| 8 | Creating Geometry: cell, layer, polygon, wire, text + GDS |
| 9 | Query and Inspect: open, ask, peek |
| 10 | Hierarchy: create ref + capstone project |

## Example file naming by week

### Week 2 (variables)

| File | Topic |
|------|-------|
| 01_set_one_variable.tcl | First `set` |
| 02_three_variables.tcl | name, school, grade |
| 03_print_with_dollar.tcl | `puts "My name is $name"` |
| 04_change_value.tcl | re-set and print |
| 05_expr_add_one.tcl | `expr {$age + 1}` |
| 06_two_strings_join.tcl | interpolation in one sentence |
| 07_numbers_and_strings.tcl | numeric vs string |
| 08_braces_literal.tcl | `{...}` when no substitution wanted |
| 09_simple_math.tcl | add/sub with expr |
| 10_report_card.tcl | **project**: three scores + total |

### Week 3 (lists)

| File | Topic |
|------|-------|
| 01_list_fruits.tcl | `list a b c` |
| 02_lindex_first.tcl | index 0 |
| 03_lindex_last.tcl | last element |
| 04_llength_count.tcl | count items |
| 05_lappend_add.tcl | append items |
| 06_print_each_manual.tcl | three lindex puts |
| 07_nested_list_intro.tcl | simple nested list |
| 08_schedule_list.tcl | class schedule data |
| 09_shopping_from_list.tcl | list as data |
| 10_today_schedule.tcl | **project**: schedule + print period N |

(Weeks 4–6: follow same 01–10 + optional 11–12 pattern from PLAN daily tasks.)

### Weeks 7–10 (Calibre)

- Reuse patterns from `examples/hello_calibre.tcl`, `create_box.tcl`, `inspect_gds.tcl`
- Run via `./scripts/run_calibre_tcl.sh lessons/N/NN_....tcl`
- Lesson docs: link PLAN manual paths and `$L` API focus for that week
- Examples may write under `tmp/`; use unique filenames per script

## Tcl file header template

```tcl
# NN_topic.tcl — Week N Day D: short description
# Run: make week<N>-NN
#      tclsh lessons/<N>/NN_topic.tcl

# --- section comment ---
# commands here
```

## Makefile block to append (week N)

```makefile
# Add to .PHONY line:
week<N> week<N>-01 week<N>-02 ... week<N>-12

# Add to help echo (optional one line):
#   make week<N>           Run all Week N examples

week<N>: check
	$(call RUN_WEEK,<N>)

week<N>-01: ; @$(MAKE) --no-print-directory run WEEK=<N> EX=01
week<N>-02: ; @$(MAKE) --no-print-directory run WEEK=<N> EX=02
# ... through last example number
```

If weeks accumulate many targets, consider documenting that `make run WEEK=N EX=NN` is the generic runner (already in Makefile).

## Lesson section skeleton (English)

```markdown
# Week N — [English Title]

> Part of the [10-week Tcl learning plan](../../PLAN.md).
> Goal this week: [from PLAN 本周目标]

## Learning goals
1. …
…

## Big idea (in everyday words)
| Tcl idea | Everyday metaphor | What you will do this week |

## What you need before you start
### Tools
### Check that Tcl works
### Run examples with Make

## Concept 1 — [first concept]
### The shape of the command
### Rules to remember
### Expected output vs what you typed
### Step-by-step walkthrough

## Concept 2 — …
(repeat for each major concept from PLAN table)

## Daily practice (≈30–45 minutes each day)
| Day | Goal | What to do in detail | Suggested file |

## Common mistakes (and fixes)
| What you see | Cause | Fix |

## Example scripts in this folder (full list)
```bash
make week<N>
make week<N>-01
…
```

## Challenge (optional, full requirements)
## Looking ahead
## Parent / teacher note
```

Chinese file: same section order, natural 小学生-friendly tone matching PLAN.md.

## Detect next week (shell)

```bash
last=$(ls -d lessons/[0-9]*/ 2>/dev/null | sed 's|lessons/||;s|/||' | sort -n | tail -1)
next=$((last + 1))
echo "Next week: $next"
```

## Verification commands

```bash
make check
make list WEEK=<N>
make week<N>
wc -l lessons/<N>/lesson_*.md
ls lessons/<N>/*.tcl | wc -l   # must be >= 10
```
