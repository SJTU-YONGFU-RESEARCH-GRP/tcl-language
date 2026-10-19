# Lab: VLSI Static Timing Analysis (STA) Report Analyzer

Bilingual practical lab on parsing industrial timing reports, calculating Worst Negative Slack (WNS) and Total Negative Slack (TNS), and automating design sign-off checks.

---

## 1. Overview (中文 / English)

### 中文
在数字集成电路设计（VLSI）流程中，静态时序分析（Static Timing Analysis, STA）是芯片流片（Tapeout）前的关键门禁（Sign-off）。工具（如 PrimeTime, Tempus, OpenSTA）会生成详尽的时序报告，工程师使用 Tcl 脚本自动遍历各时钟域与关键路径，提取起点（Startpoint）、终点（Endpoint）和时序余量（Slack），判断芯片是否满足时序收敛要求。

本实验演示如何运用 Tcl 的核心能力（文件 I/O、正则表达式、列表操作与字典 `dict`），构建一条轻量级时序报告解析流水线。

### English
In digital VLSI physical design, Static Timing Analysis (STA) is a critical sign-off checkpoint before tapeout. EDA timing engines (such as PrimeTime, Tempus, or OpenSTA) output text reports containing path delays and timing slacks. Engineers rely on Tcl automation to parse paths, detect violations, and verify timing closure.

This lab demonstrates how to use Tcl's core capabilities (file channels, regular expressions, list manipulation, and dictionaries) to parse timing reports and calculate sign-off metrics.

---

## 2. Key Concepts & Metrics

| Metric | Full Name | Definition | Sign-off Goal |
| :--- | :--- | :--- | :--- |
| **Slack** | Timing Slack | $\text{Data Required Time} - \text{Data Arrival Time}$. Positive means met; negative means timing violation. | $\text{Slack} \ge 0.0$ |
| **WNS** | Worst Negative Slack | The most negative slack across all analyzed paths in the design. | $0.0\text{ ns}$ |
| **TNS** | Total Negative Slack | The sum of all negative slacks across all violating paths. | $0.0\text{ ns}$ |

---

## 3. Lab Files & Execution

- **Script**: [`examples/timing_report_analyzer.tcl`](../examples/timing_report_analyzer.tcl)
- **Data File**: [`examples/data/sample_timing.rpt`](../examples/data/sample_timing.rpt)

Run from the repository root:

```bash
# Using Makefile
make timing-demo

# Or using tclsh directly
tclsh examples/timing_report_analyzer.tcl
```

---

## 4. Tcl Implementation Highlights

### Safe File I/O with `try ... finally`
```tcl
set fh [open $filepath r]
fconfigure $fh -encoding utf-8
try {
    while {[gets $fh line] >= 0} {
        # parse lines...
    }
} finally {
    close $fh
}
```

### Regular Expression Path Extraction
```tcl
if {[regexp {^\s*Startpoint:\s*(\S+)} $line -> sp]} { ... }
if {[regexp {^\s*slack\s*\((VIOLATED|MET)\)\s*([+-]?[0-9]*\.?[0-9]+)} $line -> status slack_val]} { ... }
```

### Structured Data Aggregation with `dict`
```tcl
dict set current_path startpoint $sp
dict set current_path endpoint   $ep
dict set current_path slack      [expr {$slack_val + 0.0}]
dict set current_path status     $status
```
