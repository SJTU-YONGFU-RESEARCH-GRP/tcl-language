# Week 12 — Advanced I/O, Channels, Glob & Subprocesses

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Master enterprise file system pipelines: modern `chan` handles, `glob` file searches, `source` inclusion, and spawning CLI subprocesses via `exec`.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `chan configure` | `chan configure $fh -translation binary` | Configure stream encodings, buffers, and linebreaks |
| `glob` | `glob -nocomplain -directory data *.csv` | Find files matching wildcard patterns |
| `file split / join` | `file join [file dirname [info script]] data` | Cross-platform filesystem path assembly |
| `source` | `source [file join $dir utils.tcl]` | Evaluate code from an external Tcl file |
| `exec` | `exec git status --porcelain` | Run external system CLI commands |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 12 Example: Batch Search and Read Telemetry CSVs
set data_dir [file join [file dirname [info script]] ".." "data"]
set csv_files [glob -nocomplain -directory $data_dir "*.csv"]

puts "Found [llength $csv_files] CSV dataset(s) in $data_dir:"
foreach f $csv_files {
    set size [file size $f]
    puts [format "  %-25s : %8d bytes" [file tail $f] $size]
}
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
