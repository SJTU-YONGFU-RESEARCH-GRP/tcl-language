---
name: content-generation
description: Generates the next Tcl lesson week for tcl-language — bilingual lesson_en.md and lesson_zh.md, at least 10 runnable .tcl examples under lessons/N/, and Makefile targets. Use when the user asks to create the next lesson, generate week content, continue the curriculum, or invoke content-generation.
---

# Content Generation — Next Tcl Lesson

Generate the **next missing week** in `lessons/` from [PLAN.md](../../PLAN.md). Follow Week 1 quality: **full detail** (no stub/minimal sections), bilingual docs, ≥10 runnable examples, Makefile integration.

## Quick start

1. **Detect target week**
   ```bash
   ls -d lessons/*/ 2>/dev/null | sort -V
   ```
   Next week = highest existing + 1. If user specifies a week, use that instead.

2. **Read sources** (in order)
   - `PLAN.md` — section `## 第 N 周 — ...` (goals, concepts, daily tasks, checklist)
   - `lessons/<N-1>/lesson_en.md` — tone, depth, section structure
   - `Makefile` — copy week-1 target pattern for the new week

3. **Create** `lessons/<N>/` with all deliverables (see checklist below).

4. **Verify**
   ```bash
   make week<N>          # all .tcl must exit 0
   make list WEEK=<N>
   ```

5. **Report** to user: files created, `make` commands, link to PLAN week title.

## Deliverables checklist

Copy and track:

```
- [ ] lessons/<N>/lesson_en.md
- [ ] lessons/<N>/lesson_zh.md
- [ ] lessons/<N>/01_*.tcl … (≥10 numbered examples, sorted)
- [ ] Makefile updated: week<N>, week<N>-01 … week<N>-<last>
- [ ] All examples run via make week<N>
- [ ] Lesson docs mention make targets
```

## Content rules

### Lesson markdown (both languages)

Mirror structure between `lesson_en.md` and `lesson_zh.md`. Required sections:

| Section | Content |
|---------|---------|
| Title + PLAN link | Week title from PLAN; link `../../PLAN.md` |
| Learning goals | 5 numbered outcomes; completion criterion |
| Big idea | Metaphor table (concept / metaphor / this-week use) |
| Prerequisites | What prior weeks assumed; tools needed |
| Concepts | Full step-by-step (not stubs); expected input/output |
| Daily practice | Day 1–5 table mapped to example files |
| Week checklist | Checkbox list for learner |
| Common mistakes | Table: symptom / cause / fix |
| Example scripts | Full list + `make week<N>-XX` block |
| Challenge | Optional project with explicit requirements |
| Looking ahead | One paragraph preview of week N+1 |
| Parent / teacher note | Environment notes (tclsh vs calibredrv) |

**Do not** use headings like "Minimal script" or "just enough". Provide complete walkthroughs, sample output blocks, and multi-step exercises.

### Tcl examples

| Rule | Detail |
|------|--------|
| Count | ≥10 files: `01_` … `10_` required; `11_`, `12_` bonus OK |
| Naming | `NN_short_topic.tcl` (two-digit prefix, snake_case) |
| Header comment | File purpose, run command (`make week<N>-NN` or `tclsh lessons/<N>/NN_....tcl`) |
| Progression | 01–04 daily basics → 05–09 practice → 10 week project → 11–12 bonus |
| Runnable | Plain `tclsh` for weeks **1–20**; weeks **≥21** use `./scripts/run_calibre_tcl.sh` when Calibre API required |
| Scope | Teach **only** this week's PLAN concepts; no jumping ahead |
| Special chars | Use `{...}` when printing `[ ]` literally (Week 1 / Week 2 quoting) |

Each example: open with `#` comments, body demonstrating one idea, output predictable when run.

### Makefile updates

Extend root [Makefile](../../Makefile):

1. Add `week<N>` using existing `RUN_WEEK` macro.
2. Add `week<N>-01` … `week<N>-<last>` aliases → `run WEEK=<N> EX=NN`.
3. Add new targets to `.PHONY` and `help` text.
4. Generic `make run WEEK=<N> EX=<NN>` already works — no change needed.

Pattern to copy from week 1:

```makefile
week2: check
	$(call RUN_WEEK,2)

week2-01: ; @$(MAKE) --no-print-directory run WEEK=2 EX=01
```

### Week-specific environment

| Weeks | Runtime |
|-------|---------|
| 1–20 (M10 + M20) | `tclsh` only |
| ≥21 (M30 + M40) | Calibre DESIGNrev batch via `./scripts/run_calibre_tcl.sh`; reference `examples/*.tcl` and PLAN Calibre API sections |

Week 21+ examples: note in lesson docs that Calibre setup uses `./scripts/setup_calibredrv.sh` (parent/teacher runs).

## Workflow detail

### Step A — Extract week spec from PLAN.md

For week N, capture from PLAN:

- Title (Chinese; derive English title)
- 本周目标 / goals
- 要学的概念 / concept table
- 每日练习 / Day 1–5 tasks
- 本周检查 / checklist
- Any code samples or API lists (Calibre: weeks ≥21)

### Step B — Plan example files before writing

Draft a table (internal or in commit message):

| File | Day | Teaches |
|------|-----|---------|
| 01_*.tcl | 1 | First concept |
| … | … | … |
| 10_*.tcl | 5 | Week project |

Ensure ≥10 distinct exercises; week project file matches Day 5 in PLAN.

### Step C — Write lesson docs

Write `lesson_en.md` first, then `lesson_zh.md` with matching sections (not machine-translated tone — natural Chinese for kids/parents per PLAN voice).

Cross-link every example file in the example table. Include both:

```bash
make week<N>-01
tclsh lessons/<N>/01_hello.tcl
```

### Step D — Implement and test

```bash
for f in lessons/<N>/*.tcl; do echo "==> $f"; tclsh "$f" || exit 1; done
make week<N>
```

Fix Tcl errors before finishing. Weeks ≥21: test with `./scripts/run_calibre_tcl.sh` if Calibre available; otherwise document skip in report.

## Week map (PLAN.md) — Tcl-first milestones

| N | Topic (short) | Milestone |
|---|---------------|-----------|
| 1 | puts, scripts, comments | M10 |
| 2 | set, $, **quoting & substitution**, expr | M10 |
| 3 | list, lindex, llength, lappend | M10 |
| 4 | if, for, foreach, while | M10 |
| 5 | proc, return, file I/O | M10 |
| 6 | `string` ensemble | M10 |
| 7 | lists advanced | M10 |
| 8 | dict / array | M10 |
| 9 | expr / eval / subst / format / scan | M10 |
| 10 | switch / catch / try + **M10 project** | M10 |
| 11 | info | M20 |
| 12 | I/O deep (chan, glob, source, exec) | M20 |
| 13 | regexp / clock | M20 |
| 14 | namespace / package / scope | M20 |
| 15 | TclOO basics | M20 |
| 16 | TclOO advanced | M20 |
| 17–19 | scripting patterns / review workshops | M20 |
| 20 | pure-Tcl capstone | M20 |
| 21 | layout create, handles | M30 |
| 22 | create cell/layer/polygon/wire/text, GDS | M30 |
| 23 | query, peek, inspect | M30 |
| 24 | create ref + Calibre graduation | M30 |
| 25–28 | iterator / flatten / filemerge / boolean | M30 |
| 29–30 | catalog B start + **M30** | M30 |
| 31–40 | Calibre encyclopedia + **M40 audit** | M40 |
| Phase C | GUI `cwbWorkBench` / macros — only after 40 | later |

Coverage checklist: [docs/COVERAGE.md](../../../docs/COVERAGE.md).  
If `lessons/<N>/` missing but PLAN has `## 第 N 周`, generate that week. For brand-new topics beyond PLAN, add the PLAN section first.

Full PLAN excerpts: [reference.md](reference.md)

## Anti-patterns

- Creating only 3–5 examples when PLAN implies a full week
- English-only or Chinese-only lesson (always both)
- "Minimal" / "stub" / "TODO" sections in learner-facing docs
- Examples that use concepts from future weeks without PLAN allowance
- Forgetting Makefile targets (user expects `make week<N>-01`)
- Skipping `make week<N>` verification

## Output report template

Tell the user:

```markdown
## Week N created

**Topic:** [title from PLAN]

**Files:**
- lessons/N/lesson_en.md, lesson_zh.md
- lessons/N/01_….tcl … [count] examples

**Run:**
make week<N>
make week<N>-01

**Next:** Week N+1 — [preview title]
```

## Additional resources

- Section templates and Makefile snippet: [reference.md](reference.md)
- Curriculum source: [PLAN.md](../../PLAN.md)
- Style reference: [lessons/1/](../../lessons/1/)
