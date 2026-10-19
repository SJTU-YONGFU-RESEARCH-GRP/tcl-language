# 项目 D · 日志诊断助手

识别有时间与级别的日志行，统计错误和警告，并在每个问题前后保留指定行数的上下文。

## 需求

- 教学日志格式为 HH:MM:SS LEVEL message，LEVEL 为 INFO、WARN 或 ERROR；校验时间范围。
- 保留从 1 开始的原始行号；忽略末尾换行，但不删除中间空行。
- 每个 WARN/ERROR 是一个问题，带前后 radius 行原始文本；重叠的上下文可重复出现。
- 格式错误的行单独列出行号，不能悄悄当 INFO；仍可作为问题的上下文。
- 空日志输出零计数；radius 必须是 0..20 的整数。

## 输入

六行教学日志：准备、读取文件、警告、重试、错误、结束。默认保留前后各一行。

模拟参数（JSON 数组表示）：```text
argv = []
argc = 0
```
没有额外预置文件。

<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
tclsh "$workshop_repo"/projects/D/solution.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

## 起始代码

```tcl
proc diagnoseLog {text {radius 1}} {
    # 返回 dict: counts incidents invalid。
    error "请实现日志解析与上下文收集"
}
proc showDiagnosis {text {radius 1}} {puts [diagnoseLog $text $radius]}
set log "09:00:00 INFO start\n09:00:01 INFO read input\n09:00:02 WARN slow read\n09:00:03 INFO retry\n09:00:04 ERROR missing result\n09:00:05 INFO stop"
showDiagnosis $log
```
## 输出样例

```text
日志诊断 (教学样本)
ERROR: 1; WARN: 1
格式错误行: 0
WARN L3: slow read
  2 | 09:00:01 INFO read input
* 3 | 09:00:02 WARN slow read
  4 | 09:00:03 INFO retry
ERROR L5: missing result
  4 | 09:00:03 INFO retry
* 5 | 09:00:04 ERROR missing result
  6 | 09:00:05 INFO stop
```
<details><summary>分步提示</summary>

split 按换行获得原始行列表，用 for 的索引生成行号；不要在开始时过滤 INFO，否则上下文和行号会改变。

先用一条短 regexp 捕获时、分、秒、级别、消息。用 scan %d 把 08 这样的时间转换为十进制。

对每个问题计算 max(0,i-radius) 到 min(末索引,i+radius)，把每行的原始文本及行号保存到 context。

</details>
<details><summary>完整参考实现</summary>

```tcl
proc diagnoseLog {text {radius 1}} {
    if {![string is integer -strict $radius] || $radius < 0 || $radius > 20} {error "上下文行数必须是 0..20 的整数"}
    set counts [dict create INFO 0 WARN 0 ERROR 0]
    set incidents {}; set invalid {}
    set text [string trimright $text "\n"]
    if {$text eq ""} {return [dict create counts $counts incidents $incidents invalid $invalid]}
    set lines [split $text "\n"]
    for {set i 0} {$i < [llength $lines]} {incr i} {
        set raw [string trimright [lindex $lines $i] "\r"]
        if {![regexp {^([0-9]{2}):([0-9]{2}):([0-9]{2}) (INFO|WARN|ERROR) (.+)$} $raw whole h m s level message] ||
            [scan $h %d] > 23 || [scan $m %d] > 59 || [scan $s %d] > 59} {
            lappend invalid [expr {$i + 1}]; continue
        }
        dict incr counts $level
        if {$level eq "INFO"} {continue}
        set context {}
        set begin [expr {max(0, $i - $radius)}]
        set end [expr {min([llength $lines] - 1, $i + $radius)}]
        for {set j $begin} {$j <= $end} {incr j} {
            lappend context [list [expr {$j + 1}] [string trimright [lindex $lines $j] "\r"]]
        }
        lappend incidents [dict create line [expr {$i + 1}] level $level message $message context $context]
    }
    return [dict create counts $counts incidents $incidents invalid $invalid]
}
proc showDiagnosis {text {radius 1}} {
    set result [diagnoseLog $text $radius]
    puts "日志诊断 (教学样本)"
    puts "ERROR: [dict get $result counts ERROR]; WARN: [dict get $result counts WARN]"
    puts "格式错误行: [llength [dict get $result invalid]]"
    if {[llength [dict get $result invalid]]} {puts "行号: [join [dict get $result invalid] {, }]"}
    foreach item [dict get $result incidents] {
        puts "[dict get $item level] L[dict get $item line]: [dict get $item message]"
        foreach row [dict get $item context] {
            lassign $row line raw
            set marker " "
            if {$line == [dict get $item line]} {set marker "*"}
            puts [format "%s %d | %s" $marker $line $raw]
        }
    }
}
set log "09:00:00 INFO start\n09:00:01 INFO read input\n09:00:02 WARN slow read\n09:00:03 INFO retry\n09:00:04 ERROR missing result\n09:00:05 INFO stop"
showDiagnosis $log
```


</details>

## 验证用例

每个用例在新的解释器中先运行完整参考实现，再运行下列用例代码；下列预期输出仅对应第二段用例代码。本地运行命令会先显示参考实现的默认演示输出，再显示该用例的输出。用例继承上面的主预置文件，并添加或覆盖本节列出的文件。

### 相邻问题与零上下文

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
showDiagnosis "10:01:00 ERROR first\n10:01:01 WARN second\n10:01:02 ERROR third\n" 0
```
本组预期输出：

```text
日志诊断 (教学样本)
ERROR: 2; WARN: 1
格式错误行: 0
ERROR L1: first
* 1 | 10:01:00 ERROR first
WARN L2: second
* 2 | 10:01:01 WARN second
ERROR L3: third
* 3 | 10:01:02 ERROR third
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/D/solution.tcl "$workshop_repo"/projects/D/case-1.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 空日志

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
showDiagnosis ""
```
本组预期输出：

```text
日志诊断 (教学样本)
ERROR: 0; WARN: 0
格式错误行: 0
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/D/solution.tcl "$workshop_repo"/projects/D/case-2.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 非法行、非法时间和边界上下文

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
showDiagnosis "bad line\n08:09:02 WARN retry\n25:00:00 ERROR impossible" 1
```
本组预期输出：

```text
日志诊断 (教学样本)
ERROR: 0; WARN: 1
格式错误行: 2
行号: 1, 3
WARN L2: retry
  1 | bad line
* 2 | 08:09:02 WARN retry
  3 | 25:00:00 ERROR impossible
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/D/solution.tcl "$workshop_repo"/projects/D/case-3.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 参数错误不隐瞒

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
catch {diagnoseLog "" -1} message; puts $message
```
本组预期输出：

```text
上下文行数必须是 0..20 的整数
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/D/solution.tcl "$workshop_repo"/projects/D/case-4.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>


## 可以继续扩展

- 支持按时间区间筛选，但保留原始行号。
- 把重叠上下文合并成窗口，并分别标注窗口中的问题行。
- 支持多种明确版本的日志格式，为每种格式写独立解析过程。
