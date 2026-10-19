# Week 10 — Control Flow, Error Handling & Milestone 10 Capstone

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M10 (Weeks 1–10: Tcl Core Syntax)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Master branching and defensive scripting: use `switch` pattern matching, and handle exceptions via `catch` and `try/trap` to achieve Milestone 10.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `switch` | `switch -glob -- $str { p1 { ... } p2 { ... } }` | Multi-branch pattern matching |
| `catch` | `catch { open $file r } err` | Trap runtime exceptions and return error code |
| `try ... on error` | `try { ... } trap {POSIX ENOENT} { ... }` | Modern structured exception handling (Tcl 8.6+) |
| `throw / error` | `error "Custom message" / throw CODE msg` | Raise intentional exceptions |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 10 Example: Safe File Reader with Structured try-trap
proc safe_read_report {filepath} {
    try {
        set fh [open $filepath r]
        set data [read $fh]
        close $fh
        return $data
    } trap {POSIX ENOENT} {msg} {
        puts ">> [WARNING]: File '$filepath' does not exist. Using fallback mock."
        return "# MOCK REPORT\nSlack: +0.25 ns"
    } on error {err} {
        puts ">> [ERROR]: Unexpected I/O failure: $err"
        return ""
    }
}

set content [safe_read_report "non_existent_timing.rpt"]
puts "Loaded content:\n$content"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
