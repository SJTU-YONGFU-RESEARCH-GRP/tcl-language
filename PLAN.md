# 小学生 Tcl 学习计划（10 周）

> 目标：先学会用 Tcl「跟电脑说话」，再学会 **面向对象（OOP）** 的想法，最后用 Tcl 控制 Calibre DESIGNrev（calibredrv）画芯片版图、读写 GDS。
>
> 每周大约 **3～5 次练习**，每次 **30～45 分钟**。不怕慢，怕不练。

---

## 学习原则（贴在墙上）

1. **先玩后懂**：先让程序跑起来，再问「为什么」。
2. **一次只学一个小招**：今天学会 `puts`，明天再学变量。
3. **写小本子**：记下命令、报错、解决办法。
4. **每天一个小作品**：哪怕只打印一行字也算胜利。
5. **大人帮忙开环境**：calibredrv 环境由家长/老师按本仓库脚本准备；你负责写脚本、看结果。

---

## 路线图（10 周总览）

| 阶段 | 周次 | 主题 | 你会得到什么 |
|------|------|------|--------------|
| 基础 Tcl | 第 1–5 周 | 打印、变量、列表、条件、循环、过程、文件 | 能独立写小 Tcl 脚本 |
| OOP | 第 6 周 | 类、对象、方法（TclOO） | 会做「会做事的小玩具」 |
| CalibreDRV | 第 7–10 周 | 启动工具、layout 对象 API、画多边形、读写 GDS | 能用面向对象的方式操作版图 |

本仓库已有示例（后面几周会用到）：

- `examples/hello_calibre.tcl` — 在 calibredrv 里打招呼
- `examples/create_box.tcl` — 画正方形并写出 GDS
- `examples/inspect_gds.tcl` — 打开 GDS 查看
- 运行方式：`./run_calibre_tcl.sh examples/某脚本.tcl`

---

## OOP 一句话地图（第 6 周起常看）

| OOP 词 | 小学生说法 | Tcl / Calibre 里长什么样 |
|--------|------------|--------------------------|
| **类（class）** | 玩具的「模具图纸」 | `oo::class create Pet { ... }` |
| **对象（object）** | 按模具做出的真实玩具 | `set cat [Pet new "Mimi"]` |
| **方法（method）** | 玩具会做的动作 | `$cat speak` |
| **属性 / 变量** | 玩具身上贴的标签（名字、颜色） | `variable name` |
| **构造** | 「刚做出来时」发生的事 | `constructor {n} { ... }` |

Calibre 里几乎一样：

```tcl
set L [layout create]    ;# 做出一个 layout「对象」
$L create cell TOP       ;# 让这个对象去做一件事（方法）
$L create layer 1
```

> 窍门：看到 `$某东西 动词 ...`，多半就是在跟一个对象说话。

---

# 第一阶段：学会 Tcl 语言（第 1–5 周）

## 第 1 周 — 电脑会说话：`puts` 与脚本文件

**本周目标**  
让电脑按你的话打印文字；知道什么是 `.tcl` 文件。

**要学的概念（用生活比喻）**

| Tcl 概念 | 生活比喻 |
|----------|----------|
| 脚本 `.tcl` | 给机器人的一张「任务清单」 |
| `puts` | 「请把这句话说出来」 |
| `#` 注释 | 给自己看的小纸条，电脑会忽略 |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 安装/确认能运行 `tclsh`；打印 `Hello, I am learning Tcl!` |
| Day 2 | 打印自己的名字、年龄、喜欢的颜色（各一行） |
| Day 3 | 写 `my_first.tcl`，里面 5 行 `puts`，用 `tclsh my_first.tcl` 运行 |
| Day 4 | 在脚本里加 `#` 注释，解释每一行在干什么 |
| Day 5 | **小作品**：打印一张「自我介绍卡」 |

**本周检查**  
能独立写出并运行一个带注释的 `.tcl` 文件。

---

## 第 2 周 — 盒子里的东西：变量与字符串

**本周目标**  
会用 `set` 存东西，用 `$` 取出来。

**要学的概念**

| Tcl 概念 | 生活比喻 |
|----------|----------|
| `set name "Amy"` | 在盒子上贴标签 `name`，里面放 `"Amy"` |
| `$name` | 打开标签为 `name` 的盒子 |
| `"..."` / `{...}` | 两种「打包文字」的方式（先会用双引号即可） |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | `set` 三个变量：名字、学校、年级；用 `puts` 打印 |
| Day 2 | 把两个变量拼成一句话：`puts "My name is $name"` |
| Day 3 | 改变量的值，再打印，观察变化 |
| Day 4 | 练习数字：年龄 +1（用 `expr`：`expr {$age + 1}`） |
| Day 5 | **小作品**：「成绩单」— 三门课分数 + 总分 |

**本周检查**  
能用变量写自我介绍，并用 `expr` 做简单加减。

---

## 第 3 周 — 一串糖果：列表（list）

**本周目标**  
会创建列表、取第几个元素、数有多少个。

**要学的概念**

| Tcl 概念 | 生活比喻 |
|----------|----------|
| `list a b c` | 一串用空格隔开的糖果 |
| `lindex $L 0` | 拿第 1 颗（从 0 开始数！） |
| `llength $L` | 数有几颗 |
| `lappend` | 再往串上加一颗 |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 做「水果清单」列表并打印 |
| Day 2 | 用 `lindex` 打印第 1、第 2、最后一项 |
| Day 3 | 用 `llength` 打印「共有 N 种水果」 |
| Day 4 | 用 `lappend` 加两种新水果 |
| Day 5 | **小作品**：「今日课表」列表 + 打印第几节课 |

**本周检查**  
能创建列表、取值、数长度、追加元素。

---

## 第 4 周 — 如果……就……：条件与循环

**本周目标**  
让程序会判断、会重复做事。

**要学的概念**

| Tcl 概念 | 生活比喻 |
|----------|----------|
| `if {条件} { ... }` | 「如果下雨，就带伞」 |
| `for` / `foreach` | 「把每颗糖果都尝一遍」 |
| `while` | 「没做完就继续做」 |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 分数 ≥ 60 打印 Pass，否则 Fail |
| Day 2 | `foreach` 遍历水果列表，每行打印一种 |
| Day 3 | `for` 打印 1 到 10 |
| Day 4 | `while`：从 5 倒数到 1，再打印「发射！」 |
| Day 5 | **小作品**：猜数字小游戏（大人可先帮写骨架） |

**本周检查**  
能写带 `if` + `foreach` 或 `for` 的小脚本。

---

## 第 5 周 — 小帮手：过程（proc）与文件

**本周目标**  
把重复动作做成「小帮手」；能读写简单文本文件。  
（为第 6 周 OOP 打基础：`proc` ≈ 还没有「主人」的动作）

**要学的概念**

| Tcl 概念 | 生活比喻 |
|----------|----------|
| `proc 名字 {参数} {身体}` | 训练一只会做事的小狗 |
| `return` | 小狗带回结果 |
| `open` / `gets` / `puts` / `close` | 打开本子、读一行、写一行、合上 |
| `file mkdir` / `file join` | 建文件夹、拼路径 |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 写 `proc greet {name} { puts "Hi $name!" }` 并调用 |
| Day 2 | 写 `proc add {a b} { return [expr {$a + $b}] }` |
| Day 3 | 把几句话写入 `tmp/diary.txt` |
| Day 4 | 读回 `tmp/diary.txt` 并打印 |
| Day 5 | **小作品**：「工具箱」— 至少 3 个 proc（问好、加法、打印列表） |

**本周检查**  
独立完成一个小脚本：含变量、列表、`if`、循环、至少一个 `proc`、读写一个文件。

**通往 OOP 的小问题（思考即可）**  
如果有很多宠物，每只都要 `greet`、`speak`，是不是希望「每只宠物自己会说话」？→ 这就是下周要学的对象。

---

# 第二阶段：面向对象 OOP（第 6 周）

## 第 6 周 — 会做事的小玩具：类、对象、方法（TclOO）

**本周目标**  
用 Tcl 自带的 **TclOO**（`oo::class`）做出「模具 → 玩具 → 让玩具做事」。  
不要求一次学会所有 OOP 术语；先会写、会改、会讲故事。

**环境**  
继续用 `tclsh`（Tcl 8.6+ 自带 TclOO，一般不必额外安装）。

**要学的概念**

| OOP / TclOO | 生活比喻 |
|-------------|----------|
| `oo::class create ...` | 画出玩具模具 |
| `variable name` | 每个玩具自己的名字标签 |
| `constructor` | 玩具刚做好时要做的事（贴好名字） |
| `method` | 玩具会的动作 |
| `ClassName new ...` | 用模具做出一个真玩具 |
| `$obj methodName` | 对这个玩具喊：「去做某某事！」 |

**最小可运行例子（照抄 → 再改）**

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
set b [Pet new "Buddy" "dog"]
$a introduce
$a speak
$b introduce
$b speak
```

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 画图：模具（类）vs 两只真宠物（对象）；标出「方法」气泡 |
| Day 2 | 在 `tclsh` 里跑通上面的 `Pet` 例子 |
| Day 3 | 给 `Pet` 加方法 `rename {newName}`，能改名字再 `introduce` |
| Day 4 | 新建类 `Robot`：属性 `name`，方法 `beep`、`move {steps}` |
| Day 5 | **小作品**：「宠物店」— 至少 1 个类、2 个对象、3 个方法；写进 `examples/my_oop_pets.tcl` |

**可选加分（大人带着试，不强制）**

- 再做一个子类感觉：`oo::class create Cat { superclass Pet ... }`（知道「更专用的模具」即可）
- 用列表装着多个对象：`foreach p [list $a $b] { $p speak }`

**本周检查（基础 + OOP 结业）**  
能用自己的话解释：类 / 对象 / 方法；能独立写出并运行一个小 TclOO 脚本。

**和下周的桥梁**  
Calibre 不会让你写 `oo::class create layout`，但它给你的 `layout` **用起来就像对象**：

```tcl
set L [layout create]   ;# 很像 Pet new
$L create cell TOP      ;# 很像 $cat speak
```

---

# 第三阶段：Tcl + CalibreDRV（第 7–10 周）

> 提醒：本阶段需要已配置好的 calibredrv 环境（见 `setup_calibredrv.sh`）。  
> 小学生主要学「写脚本 + 看结果」；GUI / VNC 由大人协助打开。  
> **带着第 6 周的 OOP 眼镜看每一行 `$L ...`。**

## 第 7 周 — 认识新教室：calibredrv，以及「layout 对象」

**本周目标**  
知道 calibredrv 是什么；会用本仓库脚本跑 Tcl；认出 layout 就是一种对象。

**要懂的大图**

```
你写的 .tcl  →  ./run_calibre_tcl.sh  →  calibredrv -shell  →  屏幕打印结果
                                      →  （可选）GUI 看版图
```

**类比**

| 东西 | 比喻 |
|------|------|
| 普通 `tclsh` | 普通教室（可练 TclOO） |
| `calibredrv -shell` | 带「画芯片」专用对象的特殊教室 |
| `layout` 对象 | 一张会听话的图纸玩具 |
| GDS 文件 | 画好的图纸文件（给工厂看的） |

**OOP 对照练习**

| 第 6 周 TclOO | 第 7 周 Calibre |
|---------------|-----------------|
| `set cat [Pet new ...]` | `set L [layout create]` |
| `$cat speak` | `$L create cell TOP` |
| 对象句柄存在变量里 | `$L` 就是 layout 的句柄 |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 大人协助：`source setup_calibredrv.sh`，确认能找到 `calibredrv` |
| Day 2 | 运行 `./run_calibre_tcl.sh examples/hello_calibre.tcl` |
| Day 3 | 复制 hello 脚本，改成打印自己的名字 + `tcl_version` |
| Day 4 | 在笔记本写对照表：Pet 对象 vs layout 对象（至少 3 行） |
| Day 5 | **小作品**：`examples/my_hello.tcl` — 自我介绍 + 用注释标出「哪里像 OOP」 |

**本周检查**  
能独立用 `./run_calibre_tcl.sh` 跑脚本，并能指出「哪个变量像对象句柄」。

---

## 第 8 周 — 空白画布到第一个方块：cell / layer / polygon / GDS

**本周目标**  
对 layout **对象** 调用方法：建 cell、建 layer、画多边形、写出 GDS。

**要学的概念**

| 概念 | 小学生说法 | OOP 说法 |
|------|------------|----------|
| layout | 一整张芯片图纸 | 对象 |
| cell | 图纸上的「房间」（如 `TOP`） | 对象管理的一部分数据 |
| layer | 彩色透明纸 | 对象管理的另一部分数据 |
| polygon | 用点连起来的形状 | 通过方法画上去 |
| `gdsout` | 把图纸存成文件 | 对象的「保存」动作 |

**对照示例**（参考 `examples/create_box.tcl`）

```tcl
set L [layout create]          ;# new 一个 layout 对象
$L create cell TOP             ;# 方法：建 cell
$L create layer 1              ;# 方法：建 layer
$L create polygon TOP 1_0 \
  0 0 \
  100 0 \
  100 100 \
  0 100                        ;# 方法：画多边形
$L gdsout $gds TOP             ;# 方法：导出 GDS
```

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 读 `create_box.tcl`，给每一行标：创建对象 / 调方法 / 普通 Tcl |
| Day 2 | 运行示例；再改尺寸 50×50、200×200 |
| Day 3 | 画长方形 100×50；输出到 `tmp/` |
| Day 4 | （可选 OOP 封装）用 TclOO 写小类 `BoxDrawer`，方法 `draw {L cell layer x1 y1 x2 y2}` 内部调用 `$L create polygon ...`——大人可协助骨架 |
| Day 5 | **小作品**：`my_box.tcl` — 自定义大小；注释里写出「谁是对象、哪些是方法」 |

**本周检查**  
能改坐标画出不同矩形并写出 GDS；能指出脚本里的对象与方法。

**可选（大人协助）**  
用 VNC/GUI 打开 `tmp/demo_box.gds`，亲眼看到方块。

---

## 第 9 周 — 打开图纸：读 GDS、检查、再用对象说话

**本周目标**  
打开已有 GDS（得到 layout 对象）；用方法检查 cell 是否存在。

**对照示例**：`examples/inspect_gds.tcl`

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 先用第 8 周脚本生成 GDS，再运行 inspect 示例 |
| Day 2 | 读懂 `layout create $gds`：用文件「唤醒」一个 layout 对象 |
| Day 3 | 练习 `$L exists cell TOP`，打印「找到了 / 没找到」 |
| Day 4 | 故意打开错误路径，学会看报错；想一想：对象还没造出来时能不能调方法？ |
| Day 5 | **小作品**：`check_my_gds.tcl` — 打开自己的 GDS 并报告状态（可用 `if`） |

**本周检查**  
能「创建对象 → 写出 → 再打开对象检查」走通一整条小路。

---

## 第 10 周 — 毕业项目：我的小小芯片图纸（含 OOP）

**本周目标**  
综合运用 Tcl + OOP 思维 + calibredrv，完成一个有故事的小项目。

**毕业项目要求（选一或组合）**

1. **双层小房子**  
   - layer 1：地基（大矩形）  
   - layer 2：屋顶（另一个矩形或多边形）  
   - 写出 GDS，再用脚本检查 `TOP` 存在  

2. **名字首字母**（简化版）  
   - 用几个矩形拼出字母（如 `L`、`T`、`H`）  
   - 全部放在 layer 1  

3. **OOP 小工厂（推荐加分）**  
   - 用 TclOO 定义类，例如 `Rect` 或 `ChipSketch`  
   - 方法示例：`addRect`、`save`、`info`  
   - 类的方法内部调用 `$L create polygon` / `$L gdsout`  
   - 主程序只负责：`set sketch [ChipSketch new ...]` → `$sketch addRect ...` → `$sketch save`

4. **命令行参数小升级**  
   - 用 `lindex $argv 0` 让用户指定输出文件名（参考 inspect 示例）

**本周日程**

| 天 | 任务 |
|----|------|
| Day 1 | 在纸上设计：图纸故事 +（可选）类有哪些方法 |
| Day 2–3 | 写 Tcl：layout 对象方法 和/或 自己的 TclOO 类 |
| Day 4 | 写检查脚本；修复报错 |
| Day 5 | **展示日**：给家人演示；说明「哪里是类/对象/方法」；脚本放进 `examples/` |

**毕业检查清单**

- [ ] 脚本能用 `./run_calibre_tcl.sh` 跑通  
- [ ] 生成了 GDS 文件  
- [ ] 有检查脚本或检查步骤  
- [ ] 能解释：变量、列表/`proc`、**类/对象/方法**、layout、cell、layer、polygon、GDS  
- [ ] （加分）用 TclOO 封装过至少一步画图或保存逻辑  

---

# 每周固定节奏（建议）

```
周一：学一个新概念（看示例 + 笔记）
周二：照着改数字/文字
周三：自己写一小段
周四：修 bug / 问问题
周五：完成本周小作品
周末：可选复习 15 分钟，或休息
```

---

# 家长 / 老师辅助清单

| 事项 | 说明 |
|------|------|
| 环境 | `source setup_calibredrv.sh`；GUI 可用 VNC/X11（见仓库脚本） |
| 运行 | 优先用 `./run_calibre_tcl.sh examples/xxx.tcl` |
| 第 1–6 周 | 只需 `tclsh`（第 6 周练 TclOO）；不必上 calibredrv |
| 第 6 周 OOP | 确认 `tclsh` 为 8.6+：`puts $tcl_version`；卡壳时先保证最小 `Pet` 例子能跑 |
| 第 7–10 周 | 协助打开 GUI；反复提醒 `$L ...` 就是「对对象喊方法」；不代替孩子改全部代码 |
| 安全 | 只在本项目目录写文件；不要改 license / EDA 安装目录 |

---

# 10 周后可以继续学什么？

1. TclOO 进阶：`superclass`（继承）、更多方法、把数据藏在对象里  
2. 更多 polygon / path / text 图形  
3. 多个 cell、层级引用（instance）——「大对象里装着小对象」  
4. 用循环 + 对象方法批量画很多小方块  
5. 阅读 Mentor/Siemens Calibre DESIGNrev Tcl 文档（大人带着翻）  
6. 把小项目整理成「作品集」：`examples/student_*.tcl`

---

# 鼓励语

> 芯片图纸很复杂，但你现在学的是：**一步一步给电脑下清楚的命令**，还能让「小玩具对象」自己会做事。  
> 第 1 周只会打印一句话，第 6 周会做面向对象的宠物，第 10 周能画出自己的版图——这已经很了不起了。  
> 报错不是失败，是电脑在跟你玩「找不同」。继续加油！
