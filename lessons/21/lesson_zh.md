# 第 21 周 — 启动方式 + API-A：`layout create` 与句柄

> 本课对应总计划：[PLAN.md](../../PLAN.md)（**M30** 第 21–30 周；第一周 Calibre）。  
> 本周目标：会跑 Calibre 脚本；理解 **句柄（handle）**；会用空 layout 和从文件打开 layout。

---

## 学习目标

学完这一周，你应该能够：

1. 用 `./scripts/run_calibre_tcl.sh lessons/21/....tcl` 运行批处理脚本。
2. 解释 **句柄**：Tcl 里代表 Calibre layout 对象的「名字/票号」。
3. 用 `set L [layout create]` 创建空 layout。
4. 用 `set L [layout create $gds]` 打开已有 GDS。
5. 在句柄上调用 `$L create cell TOP`、`$L create layer ...`。
6. 把第 15 周 OOP 和 Calibre 对应：`Pet new` ↔ `layout create`，`$cat speak` ↔ `$L create cell`。
7. 完成 `10_my_hello_layout.tcl`：自我介绍 + 空 layout + 打印句柄。

**环境：** 需要 Calibre DESIGNrev。家长/老师运行 `./scripts/setup_calibredrv.sh`（`run_calibre_tcl.sh` 会自动 source）。

---

## 大想法（戴上第 6 周的 OOP 眼镜）

| 第 6 周 TclOO | 第 21 周 Calibre | 含义 |
|---------------|-----------------|------|
| `oo::class create Pet` | （Calibre 自带 layout） | 「模具」是内建的 |
| `[Pet new "Mimi"]` | `[layout create]` | 做出新对象 |
| `$cat speak` | `$L create cell TOP` | 让对象做事 |
| `$cat` 里的对象 | `$L` 里的句柄 | 变量存「票号」 |

手册：**Tcl Objects Have Handles** — `layout create` 返回句柄，存进变量后用 `$L 方法 ...`。

---

## 三类 API（第 7–10 周地图）

| 类别 | 长什么样 | 干什么 | 本周 |
|------|----------|--------|------|
| A. layout 命令 | `layout create`、`layout peek` | 造/偷看文件 | **是** |
| B. Layout 对象方法 | `$L create polygon ...` | 在一张图纸上画和查 | 起步（cell、layer） |
| C. GUI / Workbench | `cwbWorkBench` | 控制已打开的 GUI | 第 10 周可选 |

---

## 怎么运行（不是普通 `tclsh`）

| 模式 | 命令 | 你怎么用 |
|------|------|----------|
| **批处理脚本** | `make week21-01` 或 `./scripts/run_calibre_tcl.sh lessons/21/01_....tcl` | **主要方式** |
| GUI 看 GDS | `./scripts/open_gds.sh tmp/week21_script1.gds`（需 VNC） | 家长帮忙验收 |
| 交互 shell | `calibredrv -shell` | 可选试玩 |

在项目根目录：

```bash
make week21-02
make week21
make list WEEK=7
```

---

## 概念 1 — 在 calibredrv 里打招呼（Day 2）

和第 1 周一样用 `puts`，但在 Calibre 的 Tcl 里：

```tcl
puts "hello from calibredrv Tcl"
puts "tcl_version=$tcl_version"
exit
```

批处理脚本末尾请写 `exit`，让 calibredrv 正常退出。

见 `01_hello_calibredrv.tcl`、`examples/hello_calibre.tcl`。

---

## 概念 2 — `layout create` 与句柄（Day 3）

```tcl
set L [layout create]
puts "Handle L = $L"
```

预期输出（示例）：

```text
Handle L = layout0
```

具体名字（`layout0`、`layout1` …）由 Calibre 分配。**你要做的：** 存进 `L`，后面一律用 `$L`。

### 句柄一句话

**句柄** 是 Tcl 用来指代内存里某一个 layout 对象的短票号。

---

## 概念 3 — 对象方法：`$L create cell`（Day 4–5）

官方 Script 1 骨架：

```tcl
set L [layout create]
$L create cell TOP
$L create layer 1
$L create layer 2.7
$L create polygon TOP 1_0 0 0 100 100
$L gdsout temp.gds
```

本周重点：**create** 到 layer 为止。polygon 和 GDS 细节在第 8 周。

| 命令 | 白话 |
|------|------|
| `$L create cell TOP` | 建名为 TOP 的 cell |
| `$L create layer 1` | 建 layer 1 |
| `$L create layer 2.7` | layer 2、datatype 7 |

见 `04_create_cell_top.tcl`、`05_create_layers.tcl`、`07_script1_skeleton.tcl`。

---

## 概念 4 — 从文件打开 layout（Day 4–5）

```tcl
set L [layout create $gds]
puts "Opened: $L"
```

可选参数（保留 layer/datatype 区分）：

```tcl
set L [layout create $gds -dt_expand]
```

见 `08_layout_create_from_gds.tcl`、`09_layout_dt_expand.tcl`。

---

## 概念 5 — OOP 对照表（Day 4）

记在笔记本上：

```
Pet new              ↔  layout create
$cat speak           ↔  $L create cell TOP
object.method        ↔  $L gdsout file.gds
```

见 `06_oop_comparison.tcl`。

---

## 每日练习

| 天 | 目标 | 文件 |
|----|------|------|
| Day 1 | 环境 + 手册 TOC 找 `layout create` | （与家长） |
| Day 2 | 跑 hello | `01_hello_calibredrv.tcl` |
| Day 3 | 空 layout + 句柄 | `02`、`03` |
| Day 4 | cell、layer、OOP 联系 | `04`–`06`、`08` |
| Day 5 | **小作品** | `10_my_hello_layout.tcl` |

另跑：`07_script1_skeleton.tcl`（生成 `tmp/week21_script1.gds`）。

### 本周检查清单

- [ ] 我会用 `./scripts/run_calibre_tcl.sh` 跑脚本。
- [ ] 我能用自己的话解释句柄。
- [ ] 我用过空的和从文件打开的 `layout create`。
- [ ] 我调用过 `$L create cell TOP`。
- [ ] 我把 OOP 和第 21 周的 `$L` 联系起来了。
- [ ] 我完成了 `10_my_hello_layout.tcl`。

---

## 常见错误

| 现象 | 常见原因 | 怎么办 |
|------|----------|--------|
| `invalid command name "layout"` | 用了 `tclsh` 而不是 calibredrv | 用 `make week21-NN` 或 `run_calibre_tcl.sh` |
| 忘了句柄上的 `$` | 写成 `L create cell` | 写 `$L create cell TOP` |
| 脚本结束不退出 | 没有 `exit` | 文件末尾加 `exit` |
| 打开 GDS 失败 | 文件不存在 | 先 `make week21-07` |
| 以为句柄是路径 | 句柄是 `layout0` 这类名字 | 句柄是对象票号，不是文件名 |

---

## 示例脚本

```bash
make week21-01
make week21
make run WEEK=7 EX=10
```

| 编号 | 文件 | 练习重点 |
|------|------|----------|
| 01 | `01_hello_calibredrv.tcl` | calibredrv 里 hello |
| 02 | `02_layout_create_empty.tcl` | 空 layout |
| 03 | `03_handle_explain.tcl` | 句柄说明 |
| 04 | `04_create_cell_top.tcl` | `$L create cell` |
| 05 | `05_create_layers.tcl` | layer 1 和 2.7 |
| 06 | `06_oop_comparison.tcl` | OOP ↔ Calibre |
| 07 | `07_script1_skeleton.tcl` | Script 1 + 写 GDS |
| 08 | `08_layout_create_from_gds.tcl` | 打开 GDS |
| 09 | `09_layout_dt_expand.tcl` | `-dt_expand` |
| 10 | `10_my_hello_layout.tcl` | **本周作品** |
| 11 | `11_two_layouts_two_handles.tcl` | 两个句柄 |
| 12 | `12_run_checklist.tcl` | 检查清单 |

---

## 挑战题

改写 `10_my_hello_layout.tcl`：

1. 你的真名和目标  
2. 建两个 cell：`TOP` 和 `SUB`  
3. 若做两个 layout，打印两个句柄（可参考 `11`）  
4. 先跑 `07`，再请家长用 GUI 打开 GDS  
5. 四条 `#` 注释：介绍、句柄、cell、exit  

---

## 下一周预告

**第 8 周** — 详细创建几何：polygon、wire、text，并写出 GDS。你在 `07_script1_skeleton.tcl` 里已经见过 `$L create polygon`。

---

## 给家长 / 老师

- 手册：`calbr_drv_ref` — Introduction、Getting Started、Writing Layout Viewer Scripts。
- 批处理需要 license + `setup_calibredrv.sh`；GUI 用 VNC 可选。
- 成功标准：孩子运行 `make week21-10`，读出输出里的句柄，并像「对象票号」一样解释它。
