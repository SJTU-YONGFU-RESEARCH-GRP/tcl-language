# 第 12 周 — 深度文件 I/O、管道与子进程 (chan / glob / exec)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

掌握工业级文件系统与管道控制：运用 `chan` 现代通道管理、`glob` 模式匹配文件名、`source` 模块化加载以及 `exec` 驱动外部系统工具。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `chan configure` | `chan configure $fh -translation binary` | Configure stream encodings, buffers, and linebreaks |
| `glob` | `glob -nocomplain -directory data *.csv` | Find files matching wildcard patterns |
| `file split / join` | `file join [file dirname [info script]] data` | Cross-platform filesystem path assembly |
| `source` | `source [file join $dir utils.tcl]` | Evaluate code from an external Tcl file |
| `exec` | `exec git status --porcelain` | Run external system CLI commands |

---

## 💡 示范代码与工程蓝图

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

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
