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
| CalibreDRV | 第 7–10 周 | 手册导向：创建 / 几何 / 查询 / 层次 API | 会查手册、会组合多种 `$L` API 写脚本 |

本仓库已有示例（后面几周会用到）：

- `examples/hello_calibre.tcl` — 在 calibredrv 里打招呼
- `examples/create_box.tcl` — 画正方形并写出 GDS
- `examples/inspect_gds.tcl` — 打开 GDS 查看
- `examples/my_graduation.tcl` — 第 10 周毕业作品模板（可改）
- 完整周课：`lessons/1` … `lessons/10`（双语讲义 + 例题）；导读见 `lessons/README.md`
- 运行方式：`./scripts/run_calibre_tcl.sh examples/某脚本.tcl` 或 `make weekN`

### 官方手册在哪里（大人先收藏）

本机 Mentor/Siemens 安装里已有 **Calibre DESIGNrev Reference Manual**（批处理 Tcl API 权威来源）：

| 文档 | 本机路径 |
|------|----------|
| Reference（API 大全）PDF | `/data1/eda/eda/mentor/aoi_cal_2017.2_37.29/docs_cal_2017.2_16.14/docs/pdfdocs/calbr_drv_ref.pdf` |
| Reference HTML 目录 | `/data1/eda/eda/mentor/aoi_cal_2017.2_37.29/docs_cal_2017.2_16.14/docs/htmldocs/calbr_drv_ref/calbr_drv_ref_toc.html` |
| User’s Manual PDF | `/data1/eda/eda/mentor/aoi_cal_2017.2_37.29/docs_cal_2017.2_16.14/docs/pdfdocs/calbr_drv_user.pdf` |
| 当前工具版本（setup） | `CALIBRE_HOME=/data1/eda/eda/mentor/aoi_cal_2019.2_26.18`（API 用法与手册一致；查命令以 ref 手册为准） |

手册里和本计划最相关的章节：

1. **Introduction to Using Tcl With the Calibre Layout Viewers** — handle、Tcl 对象 vs 数据库对象  
2. **Getting Started** — Interactive Shell / Batch / GUI 模式  
3. **Writing Layout Viewer Scripts** — 官方「生成新 layout」示例（Script 1）  
4. **Batch Commands for Layout Manipulation** — `layout create` / `layout peek` / `layout filemerge`  
5. **Layout Object（`$L ...`）** — 本计划第 7–10 周的核心 API  

产品介绍（非完整 API）：[Siemens Calibre DESIGNrev](https://www.siemens.com/en-us/products/ic/calibre-design/interfaces/designrev/)

> 小学生：每周只要学会表里的「本周必会 API」。大人：卡壳时在 HTML TOC 里搜命令名（如 `create polygon`）。

### 怎样查帮助（本仓库补充）

`tclsh` **没有**内建 `help` 命令；`calibredrv` 主要靠 **少写参数时打印的 Usage:** 行来教语法。本仓库整理了：

| 资源 | 用途 | 怎么用 |
|------|------|--------|
| [docs/TCL_HELP.md](docs/TCL_HELP.md) | Tcl / tclsh 怎么自学命令 | 读文档；或 `make help-tcl` |
| [docs/CALIBRE_HELP.md](docs/CALIBRE_HELP.md) | Calibre `layout` / `$L` Usage 速查 | 读文档；或 `make help-calibre` |
| `tools/show_tcl_help.tcl` | 打印本周相关 Tcl 命令名 | `tclsh tools/show_tcl_help.tcl` |
| `tools/show_calibre_help.tcl` | 向 calibredrv 追问 Usage | `./scripts/run_calibre_tcl.sh tools/show_calibre_help.tcl` |
| `lessons/N/lesson_en.md` + `lesson_zh.md` | 每周详细双语讲义 + ≥10 个例题 | `make weekN` / `make weekN-01` |

卡壳时顺序建议：**先跑例题 → 看 Usage / 报错 → 查本周 lesson → 再查手册 HTML TOC**。

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
> API 说明对齐官方 *Calibre DESIGNrev Reference Manual*（`calbr_drv_ref`）。完整语法以手册为准；下表是学习用「必会子集」。

### 手册里的三类 API（先建立地图）

| 类别 | 长什么样 | 干什么 | 本计划周次 |
|------|----------|--------|------------|
| **A. layout 命令**（全局） | `layout create` / `layout peek` / `layout filemerge` | 造图纸、偷看文件、合并文件 | 第 7、9 周 |
| **B. Layout 对象方法** | `$L create polygon ...` / `$L cells` | 对某一张图纸读写、画画、提问 | 第 7–10 周 |
| **C. GUI / Workbench**（选学） | `cwbWorkBench`、`$cwb cget -_layout` | 控制已经打开的桌面窗口 | 第 10 周可选 |

手册要点（Introduction）：**Tcl Objects Have Handles** — `layout create` 返回的句柄存进 `$L`，之后都写 `$L 方法名 ...`。  
多数几何图形本身不是独立 Tcl 对象，而是通过 `$L` 的方法创建/查询。

---

## 第 7 周 — 启动方式 + API-A：`layout create` 与句柄

**本周目标**  
会跑脚本；理解 **handle（句柄）**；会用空 layout 和从文件打开 layout。

**运行方式（手册 Getting Started）**

| 模式 | 怎么跑 | 小学生怎么用 |
|------|--------|--------------|
| Batch / shell 脚本 | `./run_calibre_tcl.sh script.tcl`（内部 `calibredrv -shell -s ...`） | **主战场** |
| 打开 GDS 看图 | `calibredrv tmp/xxx.gds`（需 DISPLAY/VNC） | 大人协助「验收」 |
| 交互 shell | `calibredrv -shell` 后手动敲命令 | 可选试玩 |

**本周必会 API**

| API | 手册含义 | 小学生说法 | 最小例子 |
|-----|----------|------------|----------|
| `layout create` | 新建空 layout，返回 handle | 拿出空白图纸 | `set L [layout create]` |
| `layout create $file` | 从 GDS/OASIS 等加载 | 打开已有图纸 | `set L [layout create $gds]` |
| （常用选项）`-dt_expand` | 保留 layer/datatype 区分 | 别把不同颜色层糊成一层 | `layout create $gds -dt_expand` |
| （常用选项）`-preserveProperties` | 保留 property | 保住图纸上的小纸条 | 大人需要时再加 |

手册还支持从 RDB、LEF/DEF、OA、Milkyway 等创建 layout——第 7 周**不必学**，知道「同一条 `layout create` 很能干」即可。

**官方 Script 1 骨架**（Writing Layout Viewer Scripts）

```tcl
set L [layout create]      ;# 空容器：还没有 cell / layer
$L create cell TOP
$L create layer 1
$L create layer 2.7        ;# layer.datatype 写法
$L create polygon TOP 1 0 0 100 100
$L gdsout temp.gds
```

本仓库对照：`examples/hello_calibre.tcl`、`examples/create_box.tcl`。

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | `source setup_calibredrv.sh`；确认 `calibredrv`；打开 HTML TOC 找 `layout create` 那一页（大人带） |
| Day 2 | 跑 `examples/hello_calibre.tcl`；抄写「句柄」三个字到笔记本 |
| Day 3 | 写脚本：空 `layout create` → 打印 `$L` → `exit` |
| Day 4 | OOP 对照表：`Pet new` vs `layout create`；`$cat speak` vs `$L create cell` |
| Day 5 | **小作品**：`my_hello.tcl` — 自我介绍 + 创建空 layout 并 `puts` 句柄 |

**本周检查**  
能解释句柄；能独立用 `./run_calibre_tcl.sh` 跑脚本。

---

## 第 8 周 — API-B 创建几何：cell / layer / polygon / wire / text + 写出文件

**本周目标**  
按手册 **Layout Object → create\*** 系列，画出多种图形并导出 GDS（或 OASIS）。

**本周必会 API（创建 + 导出）**

| API | 语法要点（手册） | 小学生说法 |
|-----|------------------|------------|
| `$L units microns ?n?` | 设置数据库单位与微米关系 | 定尺子刻度（新建 layout 时常设，如 `1000`） |
| `$L create cell name` | 建 cell | 建一个房间 |
| `$L create layer L` 或 `L.D` | 层号或 `layer.datatype` | 选一张透明彩纸 |
| `$L create polygon cell layer x1 y1 ... xn yn` | **坐标必须是一个个数字**，不是一层 list | 用点连形状 |
| `$L create wire cell layer width x1 y1 ...` | path/导线 | 画有宽度的小路 |
| `$L create text cell layer x y text` | 文字标注 | 在图上写名字 |
| `$L gdsout file ?cell?` | 写出 GDS；可只写某个 cell 层次 | 存成 GDS |
| `$L oasisout file ...` | 写出 OASIS | 另一种图纸格式（知道即可） |

**层号两种写法（都会遇到）**

| 写法 | 例子 | 说明 |
|------|------|------|
| 整数层 | `1` | 手册 Script 1 用法 |
| `layer.datatype` | `1.0` / `2.7` | 手册推荐区分 datatype |
| `layer_datatype` | `1_0` | 本仓库 `create_box.tcl` 用法；以你环境实测为准 |

**坐标 list 小陷阱（很重要）**

手册要求：`create polygon` 的坐标是展开的数字。若变量是 list，要用 `eval`：

```tcl
set coords {0 0 100 0 100 100 0 100}
eval $L create polygon TOP 1.0 $coords
# 等价于：$L create polygon TOP 1.0 0 0 100 0 100 100 0 100
```

**矩形两种写法**

```tcl
# 手册：对角两点即可表示矩形 polygon
$L create polygon TOP 1 0 0 100 100

# 或完整四角（本仓库 create_box.tcl）
$L create polygon TOP 1_0 0 0 100 0 100 100 0 100
```

**综合小例子（多 API）**

```tcl
set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1.0
$L create layer 2.0
$L create polygon TOP 1.0 0 0 100 100
$L create wire TOP 2.0 10 0 50  50 50  100 50
$L create text TOP 1.0 10 110 "HELLO"
$L gdsout tmp/week8_multi.gds TOP
```

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 跑通 `examples/create_box.tcl`；对照手册 Script 1 |
| Day 2 | 改尺寸；试 `1` / `1.0` / `1_0` 哪种在你环境可用，记下来 |
| Day 3 | 加 `$L create text` 写自己名字缩写 |
| Day 4 | 加 `$L create wire` 画一条「小路」；坐标 list + `eval` 练一次 |
| Day 5 | **小作品**：`my_shapes.tcl` — 至少用 **polygon + text**（加分：wire）；写出 `tmp/` |

**本周检查**  
能创建 cell/layer，画 ≥2 种几何，成功 `gdsout`。

**可选**  
GUI 打开 GDS 验收；试 `$L oasisout tmp/week8.oas`。

---

## 第 9 周 — API-A/B 查询：打开、提问、peek（不瞎改）

**本周目标**  
读回 GDS；用查询 API「问图纸问题」；认识 `layout peek`（不完整加载也能偷看）。

**本周必会 API（查询）**

| API | 手册含义 | 小学生说法 |
|-----|----------|------------|
| `layout create $gds` | 加载文件得到 `$L` | 打开图纸 |
| `$L topcell` | 返回 topcell 名 | 最大的房间叫什么 |
| `$L cells` | 列出 cells | 有哪些房间 |
| `$L layers` | 列出 layers | 有哪些彩纸 |
| `$L exists cell name` | cell 是否存在 | 有没有叫 TOP 的房间 |
| `$L exists layer ...` | layer 是否存在 | 有没有这层 |
| `$L bbox cell` | cell 包围盒 | 房间有多大一圈 |
| `$L file` | 关联文件名等信息 | 这张图从哪来 |
| `layout peek $gds -cells` | 不完整加载就列 cell | 隔着窗户数房间 |
| `layout peek $gds -layers` | 偷看有哪些层 | 隔着窗户看彩纸 |
| `layout peek $gds -topcell` | 偷看 topcell | 隔着窗户看大门牌 |
| `layout peek $gds -precision` / `-units` | 精度与单位 | 尺子多细 |

进阶（知道名字即可）：`$L children`、`$L iterator poly|wire|text|ref`、`$L report`。

**报告脚本模板**

```tcl
set gds [lindex $argv 0]
if {$gds eq ""} {
  set gds [file normalize [file join [file dirname [info script]] .. tmp demo_box.gds]]
}
puts "peek cells:  [layout peek $gds -cells]"
puts "peek layers: [layout peek $gds -layers]"
puts "peek top:    [layout peek $gds -topcell]"

set L [layout create $gds -dt_expand]
puts "topcell=[$L topcell]"
puts "cells=[$L cells]"
puts "layers=[$L layers]"
if {[$L exists cell TOP]} {
  puts "bbox TOP = [$L bbox TOP]"
} else {
  puts "no cell TOP"
}
exit
```

对照：`examples/inspect_gds.tcl`。

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 用第 8 周 GDS；跑 inspect；再写 `layout peek ... -cells/-layers` |
| Day 2 | 打印 `$L topcell`、`$L cells`、`$L layers` |
| Day 3 | `$L exists cell` + `$L bbox`；用 `if` 友好提示 |
| Day 4 | 对比：peek（不加载）vs `layout create`（加载）各打印一次，写一句差别 |
| Day 5 | **小作品**：`report_gds.tcl` — 接受可选路径参数，打印报告 |

**本周检查**  
能打开自己的 GDS，并用 ≥4 个查询 API 打出报告。

---

## 第 10 周 — API 层次：`create ref` + 多 API 毕业作品

**本周目标**  
学会 **cell 引用（placement）**；毕业作品至少组合 **创建 + 几何 + 查询** 三类 API。

**本周必会 API（层次）**

| API | 语法要点（手册） | 小学生说法 |
|-----|------------------|------------|
| `$L create ref incell refcell x y mirror angle mag` | 在 `incell` 里放置 `refcell` | 把零件盒摆进大厅 |
| 可选 `cols rows xspace yspace` | 阵列摆放 | 像橡皮图章盖很多个 |
| `$L children` / `$L refcount` | 看引用关系 | 谁装了谁、用了几次 |

最小层次例子：

```tcl
set L [layout create]
$L units microns 1000
$L create cell BOX
$L create layer 1.0
$L create polygon BOX 1.0 0 0 20 20

$L create cell TOP
# 在 TOP 里放两个 BOX：位置 (0,0) 与 (40,0)；不镜像；角度 0；放大 1
$L create ref TOP BOX 0 0 0 0 1
$L create ref TOP BOX 40 0 0 0 1

$L create text TOP 1.0 0 30 "TWO BOXES"
$L gdsout tmp/week10_refs.gds TOP

puts "top=[$L topcell] cells=[$L cells]"
exit
```

**毕业项目（选一，鼓励组合 API）**

1. **双层小房子** — polygon 两层 + text 门牌 + `gdsout` + report  
2. **积木阵列** — 一个小 cell + `$L create ref` 排成 2×2 或一排  
3. **首字母积木** — 多个 polygon（或多个小 cell + ref）拼字母  
4. **OOP 小工厂（加分）** — TclOO 类封装 `addRect` / `place` / `save` / `report`，内部调用 `$L ...`  
5. **GUI 选学（大人）** — 打开 DESIGNrev 后：`set wb [find objects -class cwbWorkBench]`；`set L [$wb cget -_layout]`；`puts [$L cells]`（手册 cwbWorkBench）

**本周日程**

| 天 | 任务 |
|----|------|
| Day 1 | 纸上设计：用到哪些 API（对照下方速查表打勾） |
| Day 2–3 | 实现创建 + 几何 +（推荐）`create ref` |
| Day 4 | 写 report（peek / topcell / cells / bbox）；修 bug |
| Day 5 | **展示日**：演示脚本；口述 3 个用过的 API；放入 `examples/` |

**毕业检查清单**

- [ ] `./run_calibre_tcl.sh` 跑通  
- [ ] 生成 GDS（或 OASIS）  
- [ ] 使用 ≥1 个 **创建** API、≥2 个 **几何** API、≥2 个 **查询** API  
- [ ] （推荐）使用 `$L create ref` 或阵列参数  
- [ ] 能解释：句柄、`$L 方法`、layer/datatype、GDS  
- [ ] （加分）TclOO 封装；或 GUI `cwbWorkBench` 取当前 layout  

---

# 附录 A — CalibreDRV Tcl API 学习速查（手册子集）

> 完整列表见 `calbr_drv_ref` 目录：**Layout Commands** + **Layout Object**。此处只列学习路线上的高频命令。

### A1. layout 命令（全局）

| 命令 | 用途 |
|------|------|
| `layout create` | 空库 / 打开 GDS·OASIS·RDB 等 |
| `layout peek file options...` | 不完整加载，查询 cells/layers/topcell/bbox/precision… |
| `layout filemerge -in a -in b ...` | 合并多个版图（进阶） |
| `layout delete` / `layout copy` | 删除、复制 layout 句柄（进阶） |

### A2. `$L` 创建 / 修改

| 命令 | 用途 |
|------|------|
| `$L units microns` | 单位 |
| `$L create cell` / `layer` | 结构 |
| `$L create polygon` / `wire` / `text` / `ref` | 几何与层次 |
| `$L create clip` | 按区域/RDB 裁剪（进阶） |
| `$L delete cell\|layer\|polygon\|text\|wire\|ref` | 删除（进阶，先会查再学删） |
| `$L modify origin` / `modify text` / `modify layer` | 修改（进阶） |
| `$L import layout` | 导入另一 layout（进阶） |

### A3. `$L` 导出

| 命令 | 用途 |
|------|------|
| `$L gdsout` | 写 GDS（可 `.gz`） |
| `$L oasisout` | 写 OASIS |
| `$L rdbout` / `$L asciiout` | RDB / ASCII（进阶） |

### A4. `$L` 查询 / 遍历

| 命令 | 用途 |
|------|------|
| `$L topcell` / `$L cells` / `$L layers` / `$L layernames` | 结构总览 |
| `$L exists cell\|layer` | 存在性 |
| `$L bbox` / `$L children` / `$L ancestors` | 范围与层次 |
| `$L iterator poly\|wire\|text\|ref ...` | 逐个遍历图形（进阶） |
| `$L report` / `$L query` | 报告与查询（进阶） |
| `$L scale` / `$L SIZE` / `$L SNAP` | 变换（进阶） |

### A5. GUI（选学）

| 命令 | 用途 |
|------|------|
| `find objects -class cwbWorkBench` | 找到桌面主对象 |
| `$cwb cget -_layout` | 当前打开的 layout 句柄 |
| `$cwb zoomAllClbk` / `setLayerVisibility` … | 视图控制（大人演示即可） |

---

# 附录 B — 每周 API 打卡表（可打印）

| 周 | 我练过的命令（自己打勾） |
|----|--------------------------|
| 7 | □ `layout create` □ 打印句柄 `$L` □ `./run_calibre_tcl.sh` |
| 8 | □ `units microns` □ `create cell` □ `create layer` □ `create polygon` □ `create text` □ `create wire` □ `gdsout` □（选）`oasisout` □（选）`eval`+坐标 list |
| 9 | □ `layout create $gds` □ `topcell` □ `cells` □ `layers` □ `exists cell` □ `bbox` □ `layout peek -cells/-layers/-topcell` |
| 10 | □ `create ref` □ 组合报告 □（选）TclOO 封装 □（选）`cwbWorkBench` |

---

# 每周固定节奏（建议）

```
周一：学一个新 API（手册标题 + 最小例子）
周二：照着改数字 / 层号 / 坐标
周三：自己组合 2～3 个 API
周四：修 bug / 查手册 HTML TOC
周五：完成本周小作品
周末：可选复习 15 分钟，或休息
```

---

# 家长 / 老师辅助清单

| 事项 | 说明 |
|------|------|
| 环境 | `source setup_calibredrv.sh`；GUI 用 VNC/X11（见仓库脚本） |
| 运行 | 优先 `./run_calibre_tcl.sh examples/xxx.tcl` |
| 手册 | 卡壳时打开 `calbr_drv_ref_toc.html`，搜索命令名；PDF 亦可 |
| 第 1–6 周 | 只需 `tclsh`（第 6 周 TclOO） |
| 第 7–10 周 | 强调「先查手册再猜」；层号写法以本机实测为准；不代替孩子改完全部代码 |
| 安全 | 只在本项目目录写文件；不要改 license / EDA 安装目录 |
| 进阶边界 | `filemerge`、布尔 `$L AND/OR/NOT`、RDB/OPC 流程放到 10 周后 |

---

# 进阶周（第 10 周之后，可选）

> 下面几周不是小学生必学；学会第 1–10 周即可毕业。  
> 想继续挖手册时，按顺序选修。

## 第 11 周 — 遍历图形：`$L iterator`（poly / wire / text）

**本周目标**  
用 `$L iterator` 把某个 cell、某层上的 polygon / wire / text **一个个列出来**（不只问有没有，还问「长什么样」）。

**本周必会 API**

| API | 语法要点（本机实测） | 小学生说法 |
|-----|----------------------|------------|
| `$L iterator poly cell layers range lo hi` | 例：`$L iterator poly TOP 1 range 0 end` | 把这一层的每个多边形坐标列出来 |
| `$L iterator wire cell layers range lo hi` | 例：`$L iterator wire TOP 2 range 0 end` | 列出每条导线 |
| `$L iterator text cell layers range lo hi` | 例：`$L iterator text TOP 1 range 0 end` | 列出每个文字 |
| `foreach` + iterator 结果 | 遍历返回的 list | 一行行打印 |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 打开第 8/10 周 GDS；对 TOP、layer 1 跑 `iterator poly` |
| Day 2 | 同样方式 `iterator wire` / `iterator text` |
| Day 3 | `foreach` 打印每个图形；数一数有几个 polygon |
| Day 4 | 对比：`$L layers`（清单）vs `iterator`（细节） |
| Day 5 | **小作品**：`dump_shapes.tcl` — 打开 GDS，打印 poly/wire/text 摘要 |

**本周检查**  
能对一份自己的 GDS 跑通三种 iterator，并用 `foreach` 打印。

---

# 10 周后还可以继续学什么？（手册下一站）

1. ~~`$L iterator`~~ → 见 **第 11 周**  
2. `$L flatten cell` / `expand ref`（层次展开）  
3. `layout filemerge`、`$L import layout` 做小规模拼接  
4. `$L AND` / `OR` / `NOT` / `SIZE` 等批处理几何运算  
5. RDB：`layout create xxx.rdb`、`$L rdbout`、`$L create clip`  
6. GUI 宏与 `cwbWorkBench` 回调（Writing Macros 章）  
7. TclOO 把常用流程封成自己的「小工具库」  
8. 作品集：`examples/student_*.tcl`

---

# 鼓励语

> 芯片图纸很复杂，但你现在学的是：**查手册 → 选对 API → 给 `$L` 下清楚的命令**。  
> 第 1 周只会打印一句话，第 6 周会做面向对象的宠物，第 10 周能组合多种 Calibre API 画出自己的版图——这已经很了不起了。  
> 报错不是失败，是电脑在跟你玩「找不同」。继续加油！
