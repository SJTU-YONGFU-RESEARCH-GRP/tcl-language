# Week 13 — Regular Expressions & Time Manipulation

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Master text extraction and benchmarking: capture submatches with `regexp`, perform regex substitution via `regsub`, and benchmark code with `clock`.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `regexp` | `regexp {Slack:\s+([\-\d\.]+)} $line -> slack` | Pattern matching and capture group assignment |
| `regsub` | `regsub -all {\s+} $text " " clean` | Global regular expression substitution |
| `clock seconds` | `clock seconds / clock milliseconds` | Fetch Unix epoch timestamp or millisecond ticks |
| `clock format` | `clock format [clock seconds] -format "%Y-%m-%d"` | Format timestamps into human-readable ISO dates |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 13 Example: Parse Slack and Measure Execution Time
set t0 [clock milliseconds]

set log_line "Path 14: Data arrival = 3.42 ns, Data required = 3.10 ns, Slack: -0.320 ns (VIOLATED)"
if {[regexp {Slack:\s+([\-\d\.]+)\s+ns} $log_line match slack_val]} {
    puts "Extracted Slack value: $slack_val ns"
}

set t1 [clock milliseconds]
puts "Parsed in [expr {$t1 - $t0}] ms"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
