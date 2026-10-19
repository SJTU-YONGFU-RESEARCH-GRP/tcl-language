# Week 19 — Synthesis Workshop B: Advanced I/O, Namespaces & TclOO

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Integrate Weeks 11–17 advanced features: build end-to-end pipelines combining recursive file discovery, namespace modules, and TclOO objects.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `System Integration` | `Combining glob, chan, namespace, and oo::class` | End-to-end design inspection and reporting |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 19 Example: Integrated Telemetry Parser Package
namespace eval ::eda_monitor {
    oo::class create LogWatcher {
        variable log_file
        constructor {path} { set log_file $path }
        method check_errors {} {
            if {![file exists $log_file]} { return 0 }
            set fh [open $log_file r]
            set errs 0
            while {[gets $fh line] >= 0} {
                if {[string match "*ERROR*" $line]} { incr errs }
            }
            close $fh
            return $errs
        }
    }
}
puts "LogWatcher class registered under ::eda_monitor"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
