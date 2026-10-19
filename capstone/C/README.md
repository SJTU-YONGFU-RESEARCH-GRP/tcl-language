# 项目 C · 实验测量数据统计

计算数量、最小值、最大值、平均值，并按闭区间标记越界数据；先决定空数据和非法输入的处理规则。

## 需求

- 输入是十进制数值列表，可含正负号、小数和科学计数法；拒绝 NaN、Inf、非数字和浮点溢出。
- 给定范围 lower..upper 为闭区间，端点本身不算越界；下界不得大于上界。
- 返回 count、minimum、maximum、mean、outside；outside 保存原输入的越界值。
- 空输入的 count 为 0，minimum、maximum、mean 为空值，报告显示 N/A。
- 非法数据指出一开始计数的元素序号，不能默默跳过或算成零。

## 输入

测量值 {9.5 10 10.5 13}，允许范围 9..12。全部数据是教学样本，无单位；实际实验应先统一单位。

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
tclsh "$workshop_repo"/projects/C/solution.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

## 起始代码

```tcl
proc measurementStats {values lower upper} {
    # 先检查上下界，再逐项验证和累计；空列表要单独处理。
    error "请实现 measurementStats"
}
proc showMeasurements {values lower upper} {
    puts [measurementStats $values $lower $upper]
}
showMeasurements {9.5 10 10.5 13} 9 12
```
## 输出样例

```text
数量: 4
最小值: 9.50
最大值: 13.00
平均值: 10.75
越界数: 1
越界值: 13
```
<details><summary>分步提示</summary>

写一个数值检查过程；先验证 lower 和 upper，空数据的最小值不应该伪造为 0。

首次读到数值时同时初始化 minimum、maximum；随后逐个比较，用浮点 sum 累积。

只有 count > 0 才计算 mean。将 < lower 或 > upper 的原值 lappend 到 outside，测试端点和负数。

</details>
<details><summary>完整参考实现</summary>

```tcl
proc measurementNumber {value} {
    if {![regexp {^[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$} $value]} {
        error "不是有限十进制数: $value"
    }
    set number [scan $value %f]
    if {![expr {abs($number) < Inf}]} {error "不是有限十进制数: $value"}
    return $number
}
proc measurementStats {values lower upper} {
    set lower [measurementNumber $lower]; set upper [measurementNumber $upper]
    if {$lower > $upper} {error "下界不能大于上界"}
    set count 0; set minimum ""; set maximum ""; set sum 0.0; set outside {}
    foreach raw $values {
        incr count
        if {[catch {measurementNumber $raw} value]} {error "元素 $count: $value"}
        if {$count == 1 || $value < $minimum} {set minimum $value}
        if {$count == 1 || $value > $maximum} {set maximum $value}
        set sum [expr {$sum + $value}]
        if {![expr {abs($sum) < Inf}]} {error "累计值超出浮点范围"}
        if {$value < $lower || $value > $upper} {lappend outside $raw}
    }
    set mean ""
    if {$count > 0} {set mean [expr {$sum / $count}]}
    return [dict create count $count minimum $minimum maximum $maximum mean $mean outside $outside]
}
proc showMeasurements {values lower upper} {
    set result [measurementStats $values $lower $upper]
    puts "数量: [dict get $result count]"
    foreach {key label} {minimum 最小值 maximum 最大值 mean 平均值} {
        set value [dict get $result $key]
        if {$value eq ""} {puts "$label: N/A"} else {puts [format "%s: %.2f" $label $value]}
    }
    set outside [dict get $result outside]
    puts "越界数: [llength $outside]"
    if {[llength $outside]} {puts "越界值: [join $outside {, }]"}
}
showMeasurements {9.5 10 10.5 13} 9 12
```


</details>

## 验证用例

每个用例在新的解释器中先运行完整参考实现，再运行下列用例代码；下列预期输出仅对应第二段用例代码。本地运行命令会先显示参考实现的默认演示输出，再显示该用例的输出。用例继承上面的主预置文件，并添加或覆盖本节列出的文件。

### 闭区间端点与极端正负值

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
showMeasurements {-1000000 0 1000000} -1000000 1000000
```
本组预期输出：

```text
数量: 3
最小值: -1000000.00
最大值: 1000000.00
平均值: 0.00
越界数: 0
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/C/solution.tcl "$workshop_repo"/projects/C/case-1.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 空数据

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
showMeasurements {} 0 1
```
本组预期输出：

```text
数量: 0
最小值: N/A
最大值: N/A
平均值: N/A
越界数: 0
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/C/solution.tcl "$workshop_repo"/projects/C/case-2.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 非法值、无穷、上下界反转

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
foreach bad {oops NaN Inf 1e999} {
    catch {measurementStats [list 2 $bad] 0 10} message
    puts $message
}
catch {measurementStats {1} 5 2} message
puts $message
```
本组预期输出：

```text
元素 2: 不是有限十进制数: oops
元素 2: 不是有限十进制数: NaN
元素 2: 不是有限十进制数: Inf
元素 2: 不是有限十进制数: 1e999
下界不能大于上界
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/C/solution.tcl "$workshop_repo"/projects/C/case-3.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 科学计数法与前导零按十进制解析

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
showMeasurements {09 1e1 -0.5} 0 10
```
本组预期输出：

```text
数量: 3
最小值: -0.50
最大值: 10.00
平均值: 6.17
越界数: 1
越界值: -0.5
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/C/solution.tcl "$workshop_repo"/projects/C/case-4.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>


## 可以继续扩展

- 增加中位数和样本标准差，先写明统计定义。
- 改用增量或补偿求和方法，比较大数量级数据的舍入误差。
- 让报告保留测量单位和采样时间，避免不同单位混算。
