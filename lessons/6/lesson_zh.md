# 第 6 周 — 会做事的小玩具：类、对象、方法（TclOO）

> 本课对应总计划：[10 周 Tcl 学习计划](../../PLAN.md)。  
> 本周目标：用 TclOO（`oo::class`）做出「模具 → 玩具 → 让玩具做事」。

---

## 学习目标

学完这一周，你应该能够：

1. 用自己的话解释：**类**（模具）、**对象**（真玩具）、**方法**（动作）。
2. 写 `oo::class create Pet { ... }`，含 `variable`、`constructor`、`method`。
3. 用 `[Pet new "Mimi" "cat"]` 创建对象，用 `$obj introduce` 调用方法。
4. 增加新方法（如 `rename {newName}`）并改变对象状态。
5. 再写一个类（`Robot`），含多个方法。
6. 完成 **宠物店** 小作品：1 个类、2 个以上对象、3 个以上方法。

Tcl 8.6+ 自带 TclOO，继续用 `tclsh` 即可。

---

## 大想法（用生活比喻）

| OOP / TclOO | 生活比喻 | Tcl 长什么样 |
|-------------|----------|--------------|
| 类（class） | 玩具 **模具** | `oo::class create Pet { ... }` |
| 对象（object） | 按模具做出的 **真玩具** | `set cat [Pet new "Mimi" "cat"]` |
| `variable name` | 每个玩具身上的名字标签 | 写在类体里 |
| `constructor` | 玩具刚做好时贴标签 | `constructor {n k} { set name $n }` |
| `method speak` | 玩具会的动作 | `method speak {} { ... }` |
| `$cat speak` | 「去做这个动作！」 | 对象命令 + 方法名 |

**和第 5 周对比：** `proc` 是「没有主人」的小帮手；**方法** 属于 **对象**。

**通向 Calibre（第 7 周）：** 你不会写 `oo::class create layout`，但：

```tcl
set L [layout create]   ;# 很像 Pet new
$L create cell TOP       ;# 很像 $cat speak
```

---

## 开始前需要准备什么

### 要先会的内容

- 第 1–5 周：变量、列表、`if`、循环、`proc`、文件。

### 环境

```bash
make check
```

Tcl 8.6 已包含 TclOO。

---

## 概念 1 — 类、对象、方法（Day 1–2）

### 完整 Pet 例子（来自 PLAN）

```tcl
oo::class create Pet {
    variable name kind

    constructor {n k} {
        set name $n
        set kind $k
    }

    method introduce {} {
        puts "I am $name, a $kind."
    }

    method speak {} {
        if {$kind eq "cat"} {
            puts "$name: meow!"
        } else {
            puts "$name: woof!"
        }
    }
}

set a [Pet new "Mimi" "cat"]
$a introduce
$a speak
```

### 结构说明

| 部分 | 作用 |
|------|------|
| `oo::class create Pet` | 定义名为 Pet 的类 |
| `variable name kind` | 实例变量（每个对象各有一份） |
| `constructor {n k}` | `Pet new ...` 时自动执行 |
| `method introduce {}` | 无额外参数的方法 |
| `[Pet new "Mimi" "cat"]` | 创建对象 |
| `$a introduce` | 在对象 `$a` 上调用方法 |

### 一个类，两个对象

```tcl
set a [Pet new "Mimi" "cat"]
set b [Pet new "Buddy" "dog"]
```

同一个模具（`Pet`），两个不同的玩具（`$a`、`$b`）。见 `02_pet_two_objects.tcl`。

---

## 概念 2 — 方法可以改变状态（Day 3）

```tcl
method rename {newName} {
    set name $newName
    puts "(Name changed to $name)"
}
```

调用：`$cat rename "Snowball"`，再 `$cat introduce`。

对象里的 **变量** `name` 被更新，后面的方法会看到新名字。

---

## 概念 3 — Robot 类（Day 4）

```tcl
oo::class create Robot {
    variable name steps

    constructor {n} {
        set name $n
        set steps 0
    }

    method move {count} {
        set steps [expr {$steps + $count}]
        puts "$name moved $count step(s). Total: $steps"
    }
}
```

方法可以有参数：`move {count}` → `$bot move 3`。

见 `04_robot_basic.tcl`、`05_robot_move.tcl`。

---

## 概念 4 — 宠物店小作品（Day 5）

`10_pet_shop.tcl` 包含：

- 类 `Pet`：属性 `name`、`kind`、`age`
- 方法：`introduce`、`speak`、`birthday`
- 三个对象：`$p1`、`$p2`、`$p3`

可选：复制到 `examples/my_oop_pets.tcl` 再改。

---

## 概念 5 — 加分模式

### foreach 遍历对象

```tcl
set shop [list $a $b $c]
foreach p $shop {
    $p speak
}
```

见 `09_foreach_objects.tcl`。

### 子类（可选）

```tcl
oo::class create Cat {
    superclass Pet
    method speak {} { puts "$name: meow!" }
}
```

见 `11_cat_superclass.tcl` — 更专用的模具。

---

## 每日练习

| 天 | 目标 | 文件 |
|----|------|------|
| Day 1 | 画模具 vs 玩具 vs 方法 | 纸笔 + 读 `06_class_and_object_words.tcl` |
| Day 2 | 跑通 Pet | `01_pet_basic.tcl`、`02_pet_two_objects.tcl` |
| Day 3 | 加 `rename` | `03_pet_rename.tcl` |
| Day 4 | Robot 类 | `04_robot_basic.tcl`、`05_robot_move.tcl` |
| Day 5 | **宠物店** | `10_pet_shop.tcl` |

加分：`07`–`09`、`11`、`12`。

### 本周检查清单

- [ ] 我能解释类 / 对象 / 方法。
- [ ] 我会写带 constructor、method 的 `oo::class create`。
- [ ] 我会用 `ClassName new` 创建对象。
- [ ] 我会用 `$obj methodName` 调用方法。
- [ ] 我给类加过新方法。
- [ ] 我完成了宠物店作品。

---

## 常见错误

| 现象 | 常见原因 | 怎么办 |
|------|----------|--------|
| `unknown method` | 方法名拼错 | `method speak` 与 `$obj speak` 一致 |
| 方法里名字不对 | 忘了 `variable name` | 类开头写 `variable name` |
| `invalid command name "Pet"` | 还没定义类就 `Pet new` | 先写 `oo::class create` |
| 方法里 `$name` 是空的 | constructor 没赋值 | 检查 `constructor` 体 |
| 混淆 `Pet new` 和 `$a speak` | 类和对象搞混 | `new` 在类上；方法在 `$对象` 上 |

---

## 示例脚本

```bash
make week6-01
make week6
make list WEEK=6
```

| 编号 | 文件 | 练习重点 |
|------|------|----------|
| 01 | `01_pet_basic.tcl` | 第一个 Pet 类 |
| 02 | `02_pet_two_objects.tcl` | 两个对象 |
| 03 | `03_pet_rename.tcl` | rename 方法 |
| 04 | `04_robot_basic.tcl` | Robot + beep |
| 05 | `05_robot_move.tcl` | move + 状态 |
| 06 | `06_class_and_object_words.tcl` | 词汇演示 |
| 07 | `07_constructor_args.tcl` | 多参数 constructor |
| 08 | `08_method_with_if.tcl` | method + if |
| 09 | `09_foreach_objects.tcl` | foreach 对象 |
| 10 | `10_pet_shop.tcl` | **本周作品** |
| 11 | `11_cat_superclass.tcl` | superclass 加分 |
| 12 | `12_run_checklist.tcl` | 检查清单 |

---

## 挑战题

扩展 `10_pet_shop.tcl`：

1. 增加 `feed {}` 方法  
2. 第四个宠物对象  
3. 用 `foreach` 列出所有宠物并 `speak`  
4. 一段 `#` 注释说明类 vs 对象  
5. 把完成版复制到 `examples/my_oop_pets.tcl`  

---

## 下一周预告

**第 7 周 — Calibre DESIGNrev：** `set L [layout create]` 就像做出一个 layout **对象**。你会写 `$L create cell TOP` — 同样是 **对象.方法**，只是 API 不同。

Calibre 环境由家长运行 `./scripts/setup_calibredrv.sh`；你负责写脚本、看结果。

---

## 给家长 / 老师

- OOP 术语可以先用模具 / 玩具 / 动作，不必一次讲全。
- 每个例题文件都会重新定义类 — 学习阶段这样没问题；一个文件讲一个完整故事。
- 成功标准：孩子运行 `make week6-10`，并指出哪部分是模具、哪些是玩具。
