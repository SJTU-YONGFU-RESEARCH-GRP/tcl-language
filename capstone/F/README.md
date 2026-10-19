# 项目 F · 可配置的报告生成流程

入口读取受信任配置与工具脚本，验证数据，写出摘要和错误记录；配置改变时无需改入口程序。

## 需求

- 入口从 argv 的第一个参数取得配置文件名，配置必须设置 reportConfig 字典。
- 配置包含 tools、input、output、errors、minimum；通过 source 加载受信任的配置与工具脚本。
- 工具读取 UTF-8 输入，每行格式 name,value；空行和 # 注释跳过，minimum 为有限十进制数。
- 合法记录统计总数；value >= minimum 的记录进入摘要；非法行记录原始行号和错误原因。
- 分别写出摘要文件和错误文件，使用 try/finally 关闭已打开的文件。
- 缺失文件、缺失配置字段和非法阈值必须报错；主入口通过 catch 给出错误信息。
- 浏览器文件属于每次运行创建的虚拟目录；本地执行会在当前工作目录创建实际文件。不要 source 来历不明的 Tcl 配置。

## 输入

虚拟文件包含 config.tcl、tools.tcl、readings.csv。模拟 argv 为 {config.tcl}。本地把这些文件放在同一目录，运行 tclsh solution.tcl config.tcl；CSV 仅采用本项目的两个简单字段，不支持带逗号的名称或通用带引号 CSV。

模拟参数（JSON 数组表示）：```text
argv = ["config.tcl"]
argc = 1
```
- 虚拟路径 `config.tcl` → [本地输入文件](../../data/project-F/config.tcl)

<details><summary>查看 config.tcl 的完整内容</summary>

```tcl
set reportConfig [dict create tools tools.tcl input readings.csv output summary.txt errors errors.txt minimum 10]
```


</details>

- 虚拟路径 `tools.tcl` → [本地输入文件](../../data/project-F/tools.tcl)

<details><summary>查看 tools.tcl 的完整内容</summary>

```tcl
namespace eval reportTools {
    proc decimalNumber {value} {
        if {![regexp {^[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$} $value]} {error "数值不是有限十进制数"}
        set number [scan $value %f]
        if {![expr {abs($number) < Inf}]} {error "数值不是有限十进制数"}
        return $number
    }
    proc readText {path} {
        set channel [open $path r]
        fconfigure $channel -encoding utf-8
        try {return [read $channel]} finally {close $channel}
    }
    proc writeText {path text} {
        set channel [open $path w]
        fconfigure $channel -encoding utf-8
        try {puts $channel $text} finally {close $channel}
    }
    proc summarize {text minimum} {
        set minimum [decimalNumber $minimum]
        set valid 0; set selected {}; set errors {}; set line 0
        foreach raw [split $text "\n"] {
            incr line; set raw [string trim $raw]
            if {$raw eq "" || [string match {#*} $raw]} {continue}
            set fields [split $raw ,]
            if {[llength $fields] != 2} {lappend errors "line $line: expected name,value"; continue}
            lassign $fields name value
            set name [string trim $name]; set value [string trim $value]
            if {$name eq ""} {lappend errors "line $line: empty name"; continue}
            if {[catch {decimalNumber $value} number]} {lappend errors "line $line: invalid number"; continue}
            incr valid
            if {$number >= $minimum} {lappend selected [list $name $number]}
        }
        return [dict create valid $valid selected $selected errors $errors minimum $minimum]
    }
}
```


</details>

- 虚拟路径 `readings.csv` → [本地输入文件](../../data/project-F/readings.csv)

<details><summary>查看 readings.csv 的完整内容</summary>

```text
# original teaching samples
probe-a,9.5
probe-b,12.0
probe-c,oops
probe-d,10.0
```


</details>

<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cp "$workshop_repo"/data/project-F/config.tcl "$practice_dir"/config.tcl
cp "$workshop_repo"/data/project-F/tools.tcl "$practice_dir"/tools.tcl
cp "$workshop_repo"/data/project-F/readings.csv "$practice_dir"/readings.csv
cd "$practice_dir"
tclsh "$workshop_repo"/projects/F/solution.tcl config.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

## 起始代码

```tcl
proc runReport {configPath} {
    # source 配置；检查字典及字段；source 工具；读数据；生成两个文件。
    error "请实现 runReport"
}
if {$argc != 1} {
    puts "error: usage: tclsh solution.tcl config.tcl"
} elseif {[catch {runReport [lindex $argv 0]} result]} {
    puts "error: $result"
} else {
    puts "valid=[dict get $result valid]"
}
```
## 输出样例

```text
valid=3; selected=2; errors=1
--- summary.txt ---
Teaching measurement summary
Valid: 3
Selected: 2
Minimum: 10.00
probe-b: 12.00
probe-d: 10.00
--- errors.txt ---
line 4: invalid number
```
<details><summary>分步提示</summary>

source 在当前作用域执行脚本，所以配置可用 set reportConfig ... 为 runReport 的局部变量赋值；检查字典与五个必需字段。

加载 tools.tcl 后调用 reportTools::readText 和 reportTools::summarize。将 minimum 从配置传入，不要写死为 10。

使用返回字典生成 summary 与 errors 文本，用 writeText 写出两个文件。测试新阈值、空输入、坏行、缺失文件，关闭文件要放在 finally。

</details>
<details><summary>完整参考实现</summary>

```tcl
proc runReport {configPath} {
    source -encoding utf-8 $configPath
    if {![info exists reportConfig]} {error "配置没有设置 reportConfig"}
    if {[catch {dict size $reportConfig}]} {error "reportConfig 必须是字典"}
    foreach key {tools input output errors minimum} {
        if {![dict exists $reportConfig $key]} {error "配置缺少字段: $key"}
    }
    source -encoding utf-8 [dict get $reportConfig tools]
    set minimum [reportTools::decimalNumber [dict get $reportConfig minimum]]
    set text [reportTools::readText [dict get $reportConfig input]]
    set result [reportTools::summarize $text $minimum]
    set selected [dict get $result selected]
    set summary [list "Teaching measurement summary" "Valid: [dict get $result valid]" "Selected: [llength $selected]" [format "Minimum: %.2f" $minimum]]
    foreach row $selected {
        lassign $row name value; lappend summary [format "%s: %.2f" $name $value]
    }
    set errors [dict get $result errors]
    if {![llength $errors]} {set errors [list "(none)"]}
    reportTools::writeText [dict get $reportConfig output] [join $summary "\n"]
    reportTools::writeText [dict get $reportConfig errors] [join $errors "\n"]
    dict set result output [dict get $reportConfig output]
    dict set result errorFile [dict get $reportConfig errors]
    return $result
}
if {$argc != 1} {
    puts "error: usage: tclsh solution.tcl config.tcl"
} elseif {[catch {runReport [lindex $argv 0]} result]} {
    puts "error: $result"
} else {
    puts "valid=[dict get $result valid]; selected=[llength [dict get $result selected]]; errors=[llength [dict get $result errors]]"
    puts "--- [dict get $result output] ---"
    puts [string trimright [reportTools::readText [dict get $result output]] "\n"]
    puts "--- [dict get $result errorFile] ---"
    puts [string trimright [reportTools::readText [dict get $result errorFile]] "\n"]
}
```


</details>

## 验证用例

每个用例在新的解释器中先运行完整参考实现，再运行下列用例代码；下列预期输出仅对应第二段用例代码。本地运行命令会先显示参考实现的默认演示输出，再显示该用例的输出。用例继承上面的主预置文件，并添加或覆盖本节列出的文件。

### 改变配置阈值而不修改入口

本组模拟参数：```text
argv = ["config.tcl"]
argc = 1
```
- 虚拟路径 `alternate.tcl` → [本地输入文件](../../data/project-F/case-1/alternate.tcl)

<details><summary>查看 alternate.tcl 的完整内容</summary>

```tcl
set reportConfig [dict create tools tools.tcl input alternate.csv output alternate-summary.txt errors alternate-errors.txt minimum 15]
```


</details>

- 虚拟路径 `alternate.csv` → [本地输入文件](../../data/project-F/case-1/alternate.csv)

<details><summary>查看 alternate.csv 的完整内容</summary>

```text
A,4
B,14
C,21
```


</details>

```tcl
set changed [runReport alternate.tcl]
puts "valid=[dict get $changed valid]; selected=[llength [dict get $changed selected]]; errors=[llength [dict get $changed errors]]"
puts [string trimright [reportTools::readText alternate-summary.txt] "\n"]
```
本组预期输出：

```text
valid=3; selected=1; errors=0
Teaching measurement summary
Valid: 3
Selected: 1
Minimum: 15.00
C: 21.00
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cp "$workshop_repo"/data/project-F/config.tcl "$practice_dir"/config.tcl
cp "$workshop_repo"/data/project-F/tools.tcl "$practice_dir"/tools.tcl
cp "$workshop_repo"/data/project-F/readings.csv "$practice_dir"/readings.csv
cp "$workshop_repo"/data/project-F/case-1/alternate.tcl "$practice_dir"/alternate.tcl
cp "$workshop_repo"/data/project-F/case-1/alternate.csv "$practice_dir"/alternate.csv
cd "$practice_dir"
cat "$workshop_repo"/projects/F/solution.tcl "$workshop_repo"/projects/F/case-1.tcl > run.tcl
tclsh run.tcl config.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 空文件仍生成两个文件

本组模拟参数：```text
argv = ["config.tcl"]
argc = 1
```
- 虚拟路径 `empty.tcl` → [本地输入文件](../../data/project-F/case-2/empty.tcl)

<details><summary>查看 empty.tcl 的完整内容</summary>

```tcl
set reportConfig [dict create tools tools.tcl input empty.csv output empty-summary.txt errors empty-errors.txt minimum 0]
```


</details>

- 虚拟路径 `empty.csv` → [本地输入文件](../../data/project-F/case-2/empty.csv)

<details><summary>查看 empty.csv 的完整内容</summary>

```text

```


</details>

```tcl
set empty [runReport empty.tcl]
puts [string trimright [reportTools::readText empty-summary.txt] "\n"]
puts "Errors: [string trim [reportTools::readText empty-errors.txt]]"
```
本组预期输出：

```text
Teaching measurement summary
Valid: 0
Selected: 0
Minimum: 0.00
Errors: (none)
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cp "$workshop_repo"/data/project-F/config.tcl "$practice_dir"/config.tcl
cp "$workshop_repo"/data/project-F/tools.tcl "$practice_dir"/tools.tcl
cp "$workshop_repo"/data/project-F/readings.csv "$practice_dir"/readings.csv
cp "$workshop_repo"/data/project-F/case-2/empty.tcl "$practice_dir"/empty.tcl
cp "$workshop_repo"/data/project-F/case-2/empty.csv "$practice_dir"/empty.csv
cd "$practice_dir"
cat "$workshop_repo"/projects/F/solution.tcl "$workshop_repo"/projects/F/case-2.tcl > run.tcl
tclsh run.tcl config.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 多种坏行与保留原始行号

本组模拟参数：```text
argv = ["config.tcl"]
argc = 1
```
- 虚拟路径 `bad.tcl` → [本地输入文件](../../data/project-F/case-3/bad.tcl)

<details><summary>查看 bad.tcl 的完整内容</summary>

```tcl
set reportConfig [dict create tools tools.tcl input bad.csv output bad-summary.txt errors bad-errors.txt minimum 1]
```


</details>

- 虚拟路径 `bad.csv` → [本地输入文件](../../data/project-F/case-3/bad.csv)

<details><summary>查看 bad.csv 的完整内容</summary>

```text
# input
only-one-field
,12
probe,Inf
good,1
```


</details>

```tcl
set bad [runReport bad.tcl]
puts "valid=[dict get $bad valid]; selected=[llength [dict get $bad selected]]"
puts [string trimright [reportTools::readText bad-errors.txt] "\n"]
```
本组预期输出：

```text
valid=1; selected=1
line 2: expected name,value
line 3: empty name
line 4: invalid number
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cp "$workshop_repo"/data/project-F/config.tcl "$practice_dir"/config.tcl
cp "$workshop_repo"/data/project-F/tools.tcl "$practice_dir"/tools.tcl
cp "$workshop_repo"/data/project-F/readings.csv "$practice_dir"/readings.csv
cp "$workshop_repo"/data/project-F/case-3/bad.tcl "$practice_dir"/bad.tcl
cp "$workshop_repo"/data/project-F/case-3/bad.csv "$practice_dir"/bad.csv
cd "$practice_dir"
cat "$workshop_repo"/projects/F/solution.tcl "$workshop_repo"/projects/F/case-3.tcl > run.tcl
tclsh run.tcl config.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 缺配置字段和缺输入文件

本组模拟参数：```text
argv = ["config.tcl"]
argc = 1
```
- 虚拟路径 `incomplete.tcl` → [本地输入文件](../../data/project-F/case-4/incomplete.tcl)

<details><summary>查看 incomplete.tcl 的完整内容</summary>

```tcl
set reportConfig [dict create tools tools.tcl input readings.csv output x.txt errors y.txt]
```


</details>

- 虚拟路径 `missing.tcl` → [本地输入文件](../../data/project-F/case-4/missing.tcl)

<details><summary>查看 missing.tcl 的完整内容</summary>

```tcl
set reportConfig [dict create tools tools.tcl input absent.csv output x.txt errors y.txt minimum 1]
```


</details>

```tcl
catch {runReport incomplete.tcl} message; puts $message
puts "缺失输入报错: [catch {runReport missing.tcl}]"
```
本组预期输出：

```text
配置缺少字段: minimum
缺失输入报错: 1
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cp "$workshop_repo"/data/project-F/config.tcl "$practice_dir"/config.tcl
cp "$workshop_repo"/data/project-F/tools.tcl "$practice_dir"/tools.tcl
cp "$workshop_repo"/data/project-F/readings.csv "$practice_dir"/readings.csv
cp "$workshop_repo"/data/project-F/case-4/incomplete.tcl "$practice_dir"/incomplete.tcl
cp "$workshop_repo"/data/project-F/case-4/missing.tcl "$practice_dir"/missing.tcl
cd "$practice_dir"
cat "$workshop_repo"/projects/F/solution.tcl "$workshop_repo"/projects/F/case-4.tcl > run.tcl
tclsh run.tcl config.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>


## 可以继续扩展

- 增加命令行覆盖 minimum 的选项，并验证 argc 与 argv。
- 使用 file join 将配置相对路径定位到配置所在目录，使入口可从其他目录执行。
- 为输出使用临时文件后再 rename；注明跨文件的写入仍需设计失败恢复。
