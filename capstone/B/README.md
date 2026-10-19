# 项目 B · 家庭开支摘要

用整数“分”记录金额，按类别汇总并单独报告非法记录，避免小数计算掩盖数据问题。

## 需求

- 每条输入是包含 category 和 cents 字段的字典；cents 为非负整数分。
- category 去除首尾空白后不得为空，记录不得缺字段或不是合法字典。
- 错误记录保留原序号和原因，跳过其金额；合法记录按类别累加。
- 输出合法记录数、类别金额、总额、拒绝记录数和原因；类别按字典顺序排序。
- 实现 expenseSummary 返回结构化结果，printExpenses 仅生成报告；空输入仍产生有意义的零摘要。

## 输入

五条原创教学记录：餐食 1850 分与 650 分，交通 320 分；一条负金额、一条非数字金额。使用整数分表达金额，格式化时才转换为元。

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
tclsh "$workshop_repo"/projects/B/solution.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

## 起始代码

```tcl
proc expenseSummary {records} {
    # 返回 dict: count total totals rejected。
    # rejected 是 {序号 原因} 元素的列表。
    error "请实现逐条检查和类别累加"
}
proc printExpenses {records} {
    set result [expenseSummary $records]
    puts "合法记录: [dict get $result count]"
    dict for {category cents} [dict get $result totals] {puts "$category: $cents 分"}
}
set records [list [dict create category 餐食 cents 1850] [dict create category 交通 cents 320] [dict create category 餐食 cents 650] [dict create category 日用 cents -100] [dict create category 交通 cents abc]]
printExpenses $records
```
## 输出样例

```text
合法记录: 3
交通: 3.20 元
餐食: 25.00 元
总额: 28.20 元
拒绝记录: 2
记录 4: 金额必须是非负整数分
记录 5: 金额必须是非负整数分
```
<details><summary>分步提示</summary>

为 totals、rejected、count、total 建立初始值。检查字典格式和必需字段，再读取金额，才能避免意外中断。

用 string is entier -strict 检查整数，再用 < 0 检查负数；用 dict incr totals $category $cents 累加。

将非法记录保存为 [list $index $reason] 并 continue。返回字典，在输出层才将分除以 100.0 并 format %.2f。

</details>
<details><summary>完整参考实现</summary>

```tcl
proc expenseSummary {records} {
    set totals {}; set rejected {}; set count 0; set total 0; set index 0
    foreach row $records {
        incr index
        set reason ""
        if {[catch {dict size $row}]} {
            set reason "不是合法字典"
        } elseif {![dict exists $row category] || ![dict exists $row cents]} {
            set reason "缺少 category 或 cents"
        } else {
            set category [string trim [dict get $row category]]
            set cents [dict get $row cents]
            if {$category eq ""} {
                set reason "类别为空"
            } elseif {![string is entier -strict $cents] || $cents < 0} {
                set reason "金额必须是非负整数分"
            }
        }
        if {$reason ne ""} {lappend rejected [list $index $reason]; continue}
        dict incr totals $category $cents
        incr total $cents
        incr count
    }
    return [dict create count $count total $total totals $totals rejected $rejected]
}
proc printExpenses {records} {
    set result [expenseSummary $records]
    puts "合法记录: [dict get $result count]"
    set totals [dict get $result totals]
    foreach category [lsort -dictionary [dict keys $totals]] {
        puts [format "%s: %.2f 元" $category [expr {[dict get $totals $category] / 100.0}]]
    }
    puts [format "总额: %.2f 元" [expr {[dict get $result total] / 100.0}]]
    puts "拒绝记录: [llength [dict get $result rejected]]"
    foreach item [dict get $result rejected] {
        lassign $item index reason
        puts "记录 $index: $reason"
    }
}
set records [list [dict create category 餐食 cents 1850] [dict create category 交通 cents 320] [dict create category 餐食 cents 650] [dict create category 日用 cents -100] [dict create category 交通 cents abc]]
printExpenses $records
```


</details>

## 验证用例

每个用例在新的解释器中先运行完整参考实现，再运行下列用例代码；下列预期输出仅对应第二段用例代码。本地运行命令会先显示参考实现的默认演示输出，再显示该用例的输出。用例继承上面的主预置文件，并添加或覆盖本节列出的文件。

### 换类别且允许零元

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
printExpenses [list [dict create category Book cents 1234] [dict create category " Book " cents 66] [dict create category Bus cents 0]]
```
本组预期输出：

```text
合法记录: 3
Book: 13.00 元
Bus: 0.00 元
总额: 13.00 元
拒绝记录: 0
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/B/solution.tcl "$workshop_repo"/projects/B/case-1.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 空记录集

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
printExpenses {}
```
本组预期输出：

```text
合法记录: 0
总额: 0.00 元
拒绝记录: 0
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/B/solution.tcl "$workshop_repo"/projects/B/case-2.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 格式、缺字段、空类别与小数分

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
printExpenses [list {category} [dict create category Book] [dict create category " " cents 10] [dict create category Book cents 1.5]]
```
本组预期输出：

```text
合法记录: 0
总额: 0.00 元
拒绝记录: 4
记录 1: 不是合法字典
记录 2: 缺少 category 或 cents
记录 3: 类别为空
记录 4: 金额必须是非负整数分
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/B/solution.tcl "$workshop_repo"/projects/B/case-3.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>


## 可以继续扩展

- 加日期字段，按月份和类别两级分组。
- 将拒绝记录写入独立错误文件，保留原始数据。
- 给退款设计单独的类型字段，避免悄悄把所有负数当作普通开支。
