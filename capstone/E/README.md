# 项目 E · 设计路径报告筛选器

解析原创教学路径报告，筛出负 slack 并将最严重的路径排在前面；所有数据和公式都是简化教学模型。

## 需求

- 每行格式 path=名称 delay=数值 slack=数值，数值单位 ns；空行及 # 开头的说明行跳过。
- 路径名只含字母、数字、下划线、点、冒号、斜线和连字符；delay 非负且有限，slack 有限。
- 保存非法行的行号和原因，不把它们当作合法路径。
- 默认只筛 slack < 0；按 slack 升序排序，越负越严重；相同 slack 按路径名排序。
- 输出教学声明、合法路径数、负 slack 数和结果表；空报告明确显示没有结果。
- 本项目不调用商业 EDA 命令，也不能代替真实 STA 的 setup/hold、时钟偏移、角落和不确定性分析。

## 输入

输入文件 paths.txt 中有 4 条教学路径：P_data 与 P_ctrl 负 slack，P_ok 正 slack，P_edge 为零。报告直接给出 delay/slack，不重新推断真实时序。

模拟参数（JSON 数组表示）：```text
argv = []
argc = 0
```
- 虚拟路径 `paths.txt` → [本地输入文件](../../data/project-E/paths.txt)

<details><summary>查看 paths.txt 的完整内容</summary>

```text
# Teaching path report; units: ns
path=P_data delay=9.25 slack=-1.25
path=P_ok delay=7.00 slack=1.00
path=P_ctrl delay=8.20 slack=-0.20
path=P_edge delay=8.00 slack=0.00
```


</details>

<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cp "$workshop_repo"/data/project-E/paths.txt "$practice_dir"/paths.txt
cd "$practice_dir"
tclsh "$workshop_repo"/projects/E/solution.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

## 起始代码

```tcl
proc parsePaths {text} {
    # 返回 dict: paths、rejected。
    error "请实现教学报告解析"
}
proc selectPaths {paths {threshold 0}} {
    error "请实现筛选和严重程度排序"
}
proc showPathReport {text} {puts [parsePaths $text]}
set channel [open paths.txt r]
set text [read $channel]; close $channel
showPathReport $text
```
## 输出样例

```text
教学路径报告 / ns / 非真实 STA
合法路径: 4
负 slack 路径: 2
path | delay | slack
P_data | 9.25 | -1.25
P_ctrl | 8.20 | -0.20
非法行: 0
```
<details><summary>分步提示</summary>

先按行处理，跳过空行和 # 注释；regexp 只捕获 path、delay、slack 三个字段，数值合法性另写过程判断。

将合法路径保存为 dict create name ... delay ... slack ...，非法行另存为 {行号 原因}。筛选条件用严格的 <，零 slack 不算负。

为每个入选记录构造 {slack name record}，先 lsort -dictionary -index 1，再 lsort -real -index 0，最后取 record。

</details>
<details><summary>完整参考实现</summary>

```tcl
proc pathNumber {value} {
    if {![regexp {^[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$} $value]} {error "数值必须是有限十进制数"}
    set number [scan $value %f]
    if {![expr {abs($number) < Inf}]} {error "数值必须是有限十进制数"}
    return $number
}
proc parsePaths {text} {
    set paths {}; set rejected {}; set line 0
    foreach raw [split $text "\n"] {
        incr line; set raw [string trim $raw]
        if {$raw eq "" || [string match {#*} $raw]} {continue}
        set reason ""
        if {![regexp {^path=([A-Za-z0-9_.:/-]+) +delay=(\S+) +slack=(\S+)$} $raw full name delay slack]} {
            set reason "格式不符"
        } elseif {[catch {pathNumber $delay} delayValue] || [catch {pathNumber $slack} slackValue]} {
            set reason "数值必须是有限十进制数"
        } elseif {$delayValue < 0} {
            set reason "delay 不能为负"
        }
        if {$reason ne ""} {lappend rejected [list $line $reason]; continue}
        lappend paths [dict create name $name delay $delayValue slack $slackValue]
    }
    return [dict create paths $paths rejected $rejected]
}
proc selectPaths {paths {threshold 0}} {
    set threshold [pathNumber $threshold]
    set decorated {}
    foreach path $paths {
        set slack [dict get $path slack]
        if {$slack < $threshold} {lappend decorated [list $slack [dict get $path name] $path]}
    }
    # lsort 稳定排序：先确定同 slack 时的姓名顺序，再按 slack 排。
    set decorated [lsort -dictionary -index 1 $decorated]
    set decorated [lsort -real -index 0 $decorated]
    set selected {}
    foreach item $decorated {lappend selected [lindex $item 2]}
    return $selected
}
proc showPathReport {text} {
    set result [parsePaths $text]
    set selected [selectPaths [dict get $result paths]]
    puts "教学路径报告 / ns / 非真实 STA"
    puts "合法路径: [llength [dict get $result paths]]"
    puts "负 slack 路径: [llength $selected]"
    puts "path | delay | slack"
    foreach path $selected {
        puts [format "%s | %.2f | %.2f" [dict get $path name] [dict get $path delay] [dict get $path slack]]
    }
    if {![llength $selected]} {puts "(无负 slack 路径)"}
    puts "非法行: [llength [dict get $result rejected]]"
    foreach rejected [dict get $result rejected] {
        lassign $rejected line reason; puts "行 $line: $reason"
    }
}
set channel [open paths.txt r]
set text [read $channel]; close $channel
showPathReport $text
```


</details>

## 验证用例

每个用例在新的解释器中先运行完整参考实现，再运行下列用例代码；下列预期输出仅对应第二段用例代码。本地运行命令会先显示参考实现的默认演示输出，再显示该用例的输出。用例继承上面的主预置文件，并添加或覆盖本节列出的文件。

### 严重程度排序和相同 slack 的顺序

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
showPathReport "path=Z delay=12 slack=-2\npath=A delay=12 slack=-2\npath=M delay=10.5 slack=-0.5\npath=Zero delay=10 slack=0"
```
本组预期输出：

```text
教学路径报告 / ns / 非真实 STA
合法路径: 4
负 slack 路径: 3
path | delay | slack
A | 12.00 | -2.00
Z | 12.00 | -2.00
M | 10.50 | -0.50
非法行: 0
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cp "$workshop_repo"/data/project-E/paths.txt "$practice_dir"/paths.txt
cd "$practice_dir"
cat "$workshop_repo"/projects/E/solution.tcl "$workshop_repo"/projects/E/case-1.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 空报告与仅注释

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
showPathReport "# no paths\n\n"
```
本组预期输出：

```text
教学路径报告 / ns / 非真实 STA
合法路径: 0
负 slack 路径: 0
path | delay | slack
(无负 slack 路径)
非法行: 0
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cp "$workshop_repo"/data/project-E/paths.txt "$practice_dir"/paths.txt
cd "$practice_dir"
cat "$workshop_repo"/projects/E/solution.tcl "$workshop_repo"/projects/E/case-2.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 格式错误、负 delay 与非有限数

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
showPathReport "bad line\npath=X delay=-1 slack=-2\npath=Y delay=2 slack=NaN\npath=Valid delay=2 slack=3"
```
本组预期输出：

```text
教学路径报告 / ns / 非真实 STA
合法路径: 1
负 slack 路径: 0
path | delay | slack
(无负 slack 路径)
非法行: 3
行 1: 格式不符
行 2: delay 不能为负
行 3: 数值必须是有限十进制数
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cp "$workshop_repo"/data/project-E/paths.txt "$practice_dir"/paths.txt
cd "$practice_dir"
cat "$workshop_repo"/projects/E/solution.tcl "$workshop_repo"/projects/E/case-3.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 可修改阈值但不改变数据

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
set parsed [parsePaths "path=N delay=4 slack=-0.1\npath=P delay=3 slack=0.4"]
puts "阈值 0.5: [llength [selectPaths [dict get $parsed paths] 0.5]]"
```
本组预期输出：

```text
阈值 0.5: 2
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cp "$workshop_repo"/data/project-E/paths.txt "$practice_dir"/paths.txt
cd "$practice_dir"
cat "$workshop_repo"/projects/E/solution.tcl "$workshop_repo"/projects/E/case-4.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>


## 可以继续扩展

- 增加按路径名 glob 模式过滤，保留完整输入记录。
- 增加明确的教学时钟周期字段，用 slack = period - delay 的简化模型生成样本。
- 学习真实 EDA 工具的 collection、报告格式和约束，给真实工具适配器单独编写测试。
