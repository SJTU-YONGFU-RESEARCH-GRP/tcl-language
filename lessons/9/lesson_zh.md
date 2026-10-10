# 第 9 周 — API-A/B 查询：打开、提问、peek（不瞎改）

> 本课对应总计划：[10 周 Tcl 学习计划](../../PLAN.md)。  
> 本周目标：打开 GDS，用查询 API「问图纸问题」；认识 `layout peek`（不必重画）。

**环境：** Calibre DESIGNrev。优先使用第 8 周的 GDS（`tmp/week8_my_shapes.gds`）。帮助：[docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md)。

---

## 学习目标

学完这一周，你应该能够：

1. 用 `layout peek $gds -cells/-layers/-topcell` 快速偷看。
2. 用 `set L [layout create $gds]` 打开文件（可选 `-dt_expand`）。
3. 打印 `$L topcell`、`$L cells`、`$L layers`。
4. 用 `$L exists cell` / `$L exists layer` 配合 `if` 给出友好提示。
5. 打印 `$L bbox cellName`（cell 有多大）。
6. 用一句话说明 **peek 与完整 create** 的差别。
7. 完成 **report_gds**：打印完整报告（可选路径参数）。

当你能用 ≥4 个查询 API 报告自己的第 8 周 GDS 时，第 9 周就过关了。

---

## 大想法

第 8 周 = **画图**。第 9 周 = **提问**。

| API | 生活比喻 | 本周做什么 |
|-----|----------|------------|
| `layout peek` | 隔着窗户看（不必整栋打开） | 快速查 cells/layers/top |
| `layout create $gds` | 打开屋子并拿到钥匙（`$L`） | 完整加载 |
| `$L topcell` | 最大的房间叫什么 | 名字 |
| `$L cells` / `$L layers` | 有哪些房间 / 彩纸 | 清单 |
| `$L exists …` | 有没有叫 TOP 的房间 | 是/否 |
| `$L bbox` | 房间有多大一圈 | 包围盒 |
| `$L file` | 这张图从哪个文件来 | 源路径 |

本周 **不必** 再画 polygon。用上周的 GDS 即可。

---

## 开始前需要准备什么

### 要先会的内容

- 第 7–8 周：句柄、`gdsout`、用 calibredrv 运行。

### 准备一份样例 GDS

```bash
make week8-10          # 生成 tmp/week8_my_shapes.gds
make week9-01          # 确认样例文件存在
```

---

## 概念 1 — `layout peek`（快速偷看）

```tcl
puts [layout peek $gds -cells]
puts [layout peek $gds -layers]
puts [layout peek $gds -topcell]
puts [layout peek $gds -precision]
puts [layout peek $gds -units]
```

peek **不会**给你一个长期可用的 `$L` 去调 `$L bbox`。它只回答简单问题。

见 `02_peek_cells_layers.tcl`、`03_peek_precision_units.tcl`。

---

## 概念 2 — 完整打开：`layout create $gds`

```tcl
set L [layout create $gds]
# 或保留 datatype 细节：
set L [layout create $gds -dt_expand]
puts "Handle = $L"
```

和第 7 周空 `layout create` 一样——只是纸上已经有图了。

见 `04_open_gds_handle.tcl`。

---

## 概念 3 — 向 `$L` 提问

```tcl
puts [$L topcell]
puts [$L cells]
puts [$L layers]
puts [$L file]
```

见 `05_topcell_cells_layers.tcl`、`08_exists_layer_and_file.tcl`。

---

## 概念 4 — `exists` 与 `bbox`

```tcl
if {[$L exists cell TOP]} {
    puts "bbox TOP = [$L bbox TOP]"
} else {
    puts "no cell TOP"
}
```

`bbox` 类似 `0 0 120 90`（左、下、右、上）。

见 `06_exists_cell.tcl`、`07_bbox_cell.tcl`。

---

## 概念 5 — peek 与 create 对比（Day 4）

| | `layout peek` | `layout create $gds` |
|--|---------------|----------------------|
| 轻重 | 轻 | 较重（完整加载） |
| 返回 | 直接答案 | 句柄 `$L` |
| 能调 `$L bbox`？ | 不能 | 能 |

见 `09_peek_vs_create.tcl`。

---

## 每日练习

| 天 | 目标 | 文件 |
|----|------|------|
| Day 1 | 找 GDS + peek | `01`、`02`、`03` |
| Day 2 | 打开 + 列表 | `04`、`05` |
| Day 3 | exists + bbox | `06`、`07`、`08` |
| Day 4 | 对比 peek vs create | `09` |
| Day 5 | **小作品** | `10_report_gds.tcl` |

### 本周检查清单

- [ ] peek cells / layers / topcell
- [ ] layout create $gds → 句柄
- [ ] topcell / cells / layers
- [ ] exists + bbox
- [ ] 能解释 peek vs create
- [ ] 完成 report_gds

---

## 常见错误

| 现象 | 常见原因 | 怎么办 |
|------|----------|--------|
| 找不到文件 | 没有第 8 周 GDS | `make week8-10` |
| 把 peek 结果当成 `$L` | peek 不是句柄 | 要 `$L` 方法就用 `layout create` |
| 没打开就 `exists cell` | 还没有 `$L` | 先 create |
| 路径有空格出错 | 路径没处理好 | 用 `file join` |

---

## 示例脚本

```bash
make week9-01
make week9
make week9-10
# 可选：指定别的文件
./scripts/run_calibre_tcl.sh lessons/9/10_report_gds.tcl -- tmp/week8_01_box.gds
```

| 编号 | 文件 | 练习重点 |
|------|------|----------|
| 01 | `01_find_sample_gds.tcl` | 定位 GDS |
| 02 | `02_peek_cells_layers.tcl` | peek cells/layers/top |
| 03 | `03_peek_precision_units.tcl` | peek precision/units |
| 04 | `04_open_gds_handle.tcl` | layout create $gds |
| 05 | `05_topcell_cells_layers.tcl` | `$L` 清单 |
| 06 | `06_exists_cell.tcl` | exists cell |
| 07 | `07_bbox_cell.tcl` | bbox |
| 08 | `08_exists_layer_and_file.tcl` | exists layer + file |
| 09 | `09_peek_vs_create.tcl` | 两种模式对比 |
| 10 | `10_report_gds.tcl` | **本周作品** |
| 11 | `11_compare_two_gds.tcl` | 两份 GDS peek |
| 12 | `12_run_checklist.tcl` | 检查清单 |

---

## 挑战题

扩展 `10_report_gds.tcl`：

1. 支持 `--` 后面的路径参数  
2. 没有 `TOP` 时打印清楚提示  
3. 打印 layer `1` 和 `2` 是否存在  
4. 把报告文字写到 `tmp/week9_report.txt`（用第 5 周的 `open`/`puts`/`close`）  

---

## 下一周预告

**第 10 周** — 用 `$L create ref` 做层次（把一个 cell 放进另一个），并完成多 API 毕业作品（创建 + 几何 + 查询）。

---

## 给家长 / 老师

- 本周以「只读图纸」为主；没有 GDS 时再跑第 8 周作品即可。
- 成功标准：孩子能跑 `make week9-10`，并解释一行 peek 和一行 `$L bbox`。
