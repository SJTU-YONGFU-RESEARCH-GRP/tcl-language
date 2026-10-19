# 项目 A · 报名名单清理器

把粘贴来的报名姓名变成可复核的有序名单；保留姓名里的一个空格，移除空行和重复项。

## 需求

- 输入必须是合法 Tcl 列表，每个元素代表一个完整姓名。
- 清理元素首尾空白，把连续空格、制表符和换行压成一个空格；空姓名丢弃。
- 按清理后的姓名去重；本项目区分大小写，不把不同姓名擅自合并。
- 使用 lsort -dictionary 排序，输出人数及每行一个姓名。
- 实现可复用过程 cleanRegistrations，让另一份名单也能得到正确结果。

## 输入

示例使用 list 构造六个完整姓名，包括带空格的英文姓名、重复项和空项。排序采用 Tcl 的 dictionary 顺序，不是汉语拼音排序。

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
tclsh "$workshop_repo"/projects/A/solution.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

## 起始代码

```tcl
proc cleanRegistrations {names} {
    # 1. 建立空列表；2. foreach 清理；3. 去重并排序。
    error "请实现 cleanRegistrations"
}
proc showRegistrations {names} {
    set clean [cleanRegistrations $names]
    puts "人数: [llength $clean]"
    foreach name $clean {puts $name}
}
set names [list "  Maya Chen  " "Lin Wei" "Maya\tChen" "  " "Chen Yu" "Lin  Wei"]
showRegistrations $names
```
## 输出样例

```text
人数: 3
Chen Yu
Lin Wei
Maya Chen
```
<details><summary>分步提示</summary>

先用 foreach 遍历姓名，用 string trim 去掉首尾空白。不要 split 整份名单，否则带空格的姓名会被拆开。

regsub -all {[ \t\r\n]+} $name { } name 可把连续空白替换成一个普通空格；清理后为空的项不要加入列表。

把累积列表交给 lsort -dictionary -unique；showRegistrations 只负责输出，cleanRegistrations 负责返回列表。

</details>
<details><summary>完整参考实现</summary>

```tcl
proc cleanRegistrations {names} {
    set clean {}
    foreach name $names {
        set name [string trim $name]
        regsub -all {[ \t\r\n]+} $name { } name
        if {$name ne ""} {lappend clean $name}
    }
    return [lsort -dictionary -unique $clean]
}
proc showRegistrations {names} {
    set clean [cleanRegistrations $names]
    puts "人数: [llength $clean]"
    foreach name $clean {puts $name}
}
set names [list "  Maya Chen  " "Lin Wei" "Maya\tChen" "  " "Chen Yu" "Lin  Wei"]
showRegistrations $names
```


</details>

## 验证用例

每个用例在新的解释器中先运行完整参考实现，再运行下列用例代码；下列预期输出仅对应第二段用例代码。本地运行命令会先显示参考实现的默认演示输出，再显示该用例的输出。用例继承上面的主预置文件，并添加或覆盖本节列出的文件。

### 另一份名单与姓名中的空格

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
showRegistrations [list " Zoe Li " "Ana  Park" "Zoe Li" "Ana\tPark" "Kai"]
```
本组预期输出：

```text
人数: 3
Ana Park
Kai
Zoe Li
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/A/solution.tcl "$workshop_repo"/projects/A/case-1.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 空列表和全部空白

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
showRegistrations {}; showRegistrations [list " " "\t\n"]
```
本组预期输出：

```text
人数: 0
人数: 0
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/A/solution.tcl "$workshop_repo"/projects/A/case-2.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 非法列表明确报错

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
set malformed [format %c 123]
puts "非法列表: [catch {cleanRegistrations $malformed}]"
```
本组预期输出：

```text
非法列表: 1
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/A/solution.tcl "$workshop_repo"/projects/A/case-3.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>

### 大小写规则透明

本组模拟参数：```text
argv = []
argc = 0
```
没有额外预置文件。

```tcl
showRegistrations [list "Alex" "alex" "Alex"]
```
本组预期输出：

```text
人数: 2
Alex
alex
```
<details><summary>本地准备与运行（Tcl 8.6+）</summary>

```sh
# 从本仓库根目录执行；每组运行使用一个新的临时练习目录。
workshop_repo="$PWD"
practice_dir="$(mktemp -d)"
cd "$practice_dir"
cat "$workshop_repo"/projects/A/solution.tcl "$workshop_repo"/projects/A/case-4.tcl > run.tcl
tclsh run.tcl
# 结果文件保存在上面的 practice_dir；运行结束后回到仓库。
cd "$workshop_repo"
```


</details>


## 可以继续扩展

- 增加人工确认的大小写合并开关，先展示可能冲突的姓名。
- 读取每行一个姓名的 UTF-8 文件，写出清理结果和被丢弃行号。
- 保留原始姓名到规范姓名的对照表，方便核对。
