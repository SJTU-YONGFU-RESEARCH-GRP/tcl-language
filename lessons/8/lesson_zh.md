# 第 8 周 — API-B 创建几何：cell / layer / polygon / wire / text + 写出文件

> 本课对应总计划：[10 周 Tcl 学习计划](../../PLAN.md)。  
> 本周目标：用 `$L create …` 画图形，并导出 GDS 文件。

**环境：** 与第 7 周相同，需要 Calibre DESIGNrev。用 `make week8-01` 或 `./scripts/run_calibre_tcl.sh` 运行。帮助文档：[docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md)。

---

## 学习目标

学完这一周，你应该能够：

1. 用 `$L units microns 1000` 设置单位。
2. 创建 cell 和 layer（`create cell`、`create layer`）。
3. 用 `$L create polygon` 画矩形/多边形。
4. 用 `$L create text` 加文字标注。
5. （加分）用 `$L create wire` 画有宽度的路径。
6. 需要时用 `eval` 展开坐标列表。
7. 用 `$L gdsout` 把图写到 `tmp/`。
8. 完成 **my_shapes**：至少 **polygon + text**（wire 可选）。

---

## 大想法

| API | 生活比喻 | 本周做什么 |
|-----|----------|------------|
| `$L units microns` | 定尺子刻度 | 新建空 layout 时常设 |
| `$L create cell` | 建一个房间 | 通常叫 `TOP` |
| `$L create layer` | 选一张透明彩纸 | `1` 或 `1.0` |
| `$L create polygon` | 用点连成形状 | 盒子 / 房间 |
| `$L create wire` | 画有宽度的小路 | 导线 / 路径 |
| `$L create text` | 在图上写名字 | 标注 |
| `$L gdsout` | 把图纸存盘 | 文件放在 `tmp/` |

继续戴着第 7 周的 OOP 眼镜：`$L create polygon ...` 仍是「对象.方法」。

---

## 开始前需要准备什么

### 要先会的内容

- 第 7 周：`layout create`、句柄 `$L`、`create cell`、用 `run_calibre_tcl.sh` 跑脚本。

### 工具

```bash
make check-calibre
make week8-01
```

查看 GDS（请家长帮忙）：若已配好 VNC，可用 `./scripts/open_gds.sh tmp/week8_01_box.gds`。

---

## 概念 1 — 单位与房间准备

```tcl
set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1
```

`units microns 1000` 表示：1000 个数据库单位 = 1 微米。新建 layout 时常先设这一行。

见 `02_units_microns.tcl`。

---

## 概念 2 — 层号写法（很重要）

在 **本机** Calibre 上实测：

| 写法 | `create layer` | `create polygon` |
|------|----------------|------------------|
| `1` | 可以 | 可以 |
| `1.0` | 可以 | 可以 |
| `1_0` | **不能** 用于 create layer | 层建好后，polygon 可以用 |

`examples/create_box.tcl` 的做法是：先 `create layer 1`，再 `create polygon TOP 1_0 ...`。

一个脚本里选定一种写法，尽量不要混用。见 `03_layer_styles.tcl`。

---

## 概念 3 — 多边形的两种画法

### 对角两点（手册 Script 1）

```tcl
$L create polygon TOP 1 0 0 100 100
```

两个对角点 → 矩形。

### 四个角点（明确列出）

```tcl
$L create polygon TOP 1_0 0 0 100 0 100 100 0 100
```

同样的形状，但把每个角都写出来。见 `04`、`05`。

---

## 概念 4 — 文字与导线

```tcl
$L create text TOP 1 10 110 HELLO
$L create wire TOP 2_0 10 0 0 100 0 100 50
```

| 命令 | 含义 |
|------|------|
| `create text cell layer x y 字符串` | 在 (x,y) 写标注 |
| `create wire cell L_D 宽度 x1 y1 ...` | 有宽度的路径 |

见 `06_create_text.tcl`、`07_create_wire.tcl`。

---

## 概念 5 — 坐标列表 + `eval`（陷阱！）

`create polygon` 要的是 **一个个展开的数字**，不要把一整串坐标塞成「一层 list」。

```tcl
set coords {0 0 40 0 40 30 0 30}
eval $L create polygon TOP 1 $coords
```

`eval` 会把 `$coords` 展开成多个参数。见 `08_eval_coords_list.tcl` 和 `examples/script.tcl`。

---

## 概念 6 — 导出 GDS（可选 OASIS）

```tcl
$L gdsout tmp/week8_my_shapes.gds TOP
# 可选：
$L oasisout tmp/week8.oas TOP
```

文件请写到项目的 `tmp/` 目录。见 `11_oasisout_optional.tcl`。

---

## 每日练习

| 天 | 目标 | 文件 |
|----|------|------|
| Day 1 | 像 create_box 一样画盒子 | `01_create_box_like.tcl`、`02_units_microns.tcl` |
| Day 2 | 层号写法 + 改尺寸 | `03_layer_styles.tcl`、`04`–`05` |
| Day 3 | 文字标注 | `06_create_text.tcl` |
| Day 4 | wire + eval | `07_create_wire.tcl`、`08_eval_coords_list.tcl` |
| Day 5 | **小作品** | `10_my_shapes.tcl` |

### 本周检查清单

- [ ] units / cell / layer
- [ ] polygon（盒子）
- [ ] text
- [ ] wire（或至少试一次）
- [ ] eval + 坐标列表
- [ ] gdsout 到 `tmp/`
- [ ] 完成 `10_my_shapes.tcl`

---

## 常见错误

| 现象 | 常见原因 | 怎么办 |
|------|----------|--------|
| `create layer` 报 `Unrecognized ... (1_0)` | 本机不能用 `1_0` 建层 | 改用 `create layer 1` 或 `1.0` |
| 坐标放在一个 list 里 polygon 失败 | 参数没展开 | `eval $L create polygon ... $coords` |
| `invalid command name "layout"` | 用了 tclsh | 改用 `make week8-NN` |
| tmp 里找不到文件 | 路径不对 | 按例题写到项目根下的 `tmp/` |

---

## 示例脚本

```bash
make week8-01
make week8
make list WEEK=8
```

| 编号 | 文件 | 练习重点 |
|------|------|----------|
| 01 | `01_create_box_like.tcl` | 经典盒子 → GDS |
| 02 | `02_units_microns.tcl` | units |
| 03 | `03_layer_styles.tcl` | 1 / 1.0 / 1_0 |
| 04 | `04_polygon_diagonal.tcl` | 对角矩形 |
| 05 | `05_polygon_four_corners.tcl` | 四角多边形 |
| 06 | `06_create_text.tcl` | text |
| 07 | `07_create_wire.tcl` | wire |
| 08 | `08_eval_coords_list.tcl` | eval |
| 09 | `09_multi_shapes.tcl` | 三种图形一起 |
| 10 | `10_my_shapes.tcl` | **本周作品** |
| 11 | `11_oasisout_optional.tcl` | OASIS 加分 |
| 12 | `12_run_checklist.tcl` | 检查清单 |

---

## 挑战题

改写 `10_my_shapes.tcl`：

1. 文字改成你的姓名缩写  
2. 换一个盒子尺寸  
3. 画一条穿过盒子的 wire  
4. `gdsout` 后打印文件大小  
5. （可选）再写一份 `oasisout`  

---

## 下一周预告

**第 9 周** — 不重画，只提问：`layout peek`、`$L cells`、`$L layers`、`$L bbox`、`$L exists`。你会打开本周生成的 GDS，问它「有哪些房间、多大」。

---

## 给家长 / 老师

- 层号写法因环境而异；本机建议 `create layer 1`，polygon 可用 `1` / `1.0` / `1_0`。
- GUI 打开 GDS 只作验收，非必须。
- 成功标准：孩子能跑 `make week8-10`，在 `tmp/` 看到 GDS，并能说出 polygon 和 text 的区别。
