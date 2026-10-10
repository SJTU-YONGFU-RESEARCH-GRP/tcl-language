# 第 28 周 — 图形运算：`$L AND` / `OR` / `NOT` / `SIZE`

> [10 周计划](../../PLAN.md) 之后的选修进阶周。  
> 目标：两层相交、合并、相减，以及外形放大/缩小一圈。

**环境：** Calibre DESIGNrev。帮助：[docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md)。

---

## 学习目标

1. 在 layer 1、2 上画出两个重叠的多边形。
2. 跑 `$L AND 1 2 3`，用 `iterator poly` 看结果。
3. 同样会做 `OR`、`NOT`。
4. 用 `$L SIZE 1 3 by 0.001` / `by -0.001` 放大/缩小（配合 `units microns 1000`）。
5. 完成 **boolean_poster**：`tmp/week28_poster.gds` + 报告。

---

## 大图景

| 运算 | 生活说法 | 结果 |
|------|----------|------|
| AND | 两张贴纸重叠 | 只留重叠区 |
| OR | 两张贴纸粘一起 | 一个大轮廓 |
| NOT | 用 B 去剪 A | A 被咬掉一块 |
| SIZE | 气球变胖/变瘦 | 外轮廓胀或缩 |
| XOR | 只留「独有」部分 | 两边去掉重叠 |

---

## 先修

- 第 8 周：层 + 多边形
- 第 11 周：`iterator poly` 检查结果
- Calibre：`./scripts/run_calibre_tcl.sh`

---

## 概念 1 — 重叠输入

```tcl
$L create polygon TOP 1_0 0 0 20 20
$L create polygon TOP 2_0 10 10 30 30
# 重叠大约 (10,10)-(20,20)
```

见 `01_build_overlap.tcl`。

---

## 概念 2 — AND / OR / NOT / XOR

```tcl
$L AND 1 2 3          ;# 相交 → 层 3
$L OR  1 2 4          ;# 合并 → 层 4
$L NOT 1 2 5          ;# L1 减 L2 → 层 5
$L XOR 1 2 6          ;# 异或 → 层 6
```

Usage 形态（AND/NOT/XOR）：

```
$L AND <in1> <in2> <out> [-cell <cell> [-hier 0|1]]
```

层号用数字（`1 2 3`），不要写 `1_0`。输出层要先 `create layer`。

见 `03_and.tcl` … `06_xor.tcl`、`11_compare_all.tcl`。

---

## 概念 3 — SIZE 放大 / 缩小

```tcl
$L units microns 1000
$L SIZE 1 3 by 0.001    ;# 大约 +1µm
$L SIZE 1 3 by -0.001   ;# 大约 −1µm（缩小）
```

本机可用：`$L SIZE <in> <out> by <amount>`。

**注意：** `by 1` 会大得离谱，请从 `0.001` 开始。

见 `07_size_grow.tcl`、`08_size_shrink.tcl`。

---

## 概念 4 — `-cell`

```tcl
$L AND 1 2 3 -cell TOP
```

只对某个 cell 运算。见 `09_and_cell.tcl`。

---

## 每日练习

| 天 | 目标 | 文件 |
|----|------|------|
| 1 | 重叠 + AND | `01`、`02`、`03` |
| 2 | OR + NOT | `04`、`05` |
| 3 | SIZE 放大/缩小 | `07`、`08` |
| 4 | XOR + `-cell` | `06`、`09`、`11` |
| 5 | **boolean_poster** | `10` |

### 检查清单

- [ ] AND 重叠  
- [ ] OR / NOT  
- [ ] SIZE ±0.001  
- [ ] 选修 XOR / `-cell`  
- [ ] 海报 GDS + 报告  

---

## 常见错误

| 现象 | 改法 |
|------|------|
| `Expected <inlayer1>…` | 顺序是 `in1 in2 out`，前面不要加 cell 名 |
| SIZE 空结果 / 巨大方块 | 用 `by 0.001`，不要 `by 1` |
| 输出层没有图形 | 先 `create layer` 输出层 |
| 别的 cell 也被改了 | 加上 `-cell TOP` |

---

## 示例脚本

```bash
make week28-01
make week28
make week28-10
```

| # | 文件 | 重点 |
|---|------|------|
| 01 | `01_build_overlap.tcl` | 输入 |
| 02 | `02_boolean_usage.tcl` | Usage |
| 03 | `03_and.tcl` | AND |
| 04 | `04_or.tcl` | OR |
| 05 | `05_not.tcl` | NOT |
| 06 | `06_xor.tcl` | XOR |
| 07 | `07_size_grow.tcl` | SIZE 放大 |
| 08 | `08_size_shrink.tcl` | SIZE 缩小 |
| 09 | `09_and_cell.tcl` | `-cell` |
| 10 | `10_boolean_poster.tcl` | **本周小作品** |
| 11 | `11_compare_all.tcl` | 数量对照表 |
| 12 | `12_run_checklist.tcl` | 检查清单 |

---

## 挑战题

画一个「环」：两层 OR 成大块，再用第三层小方块做 NOT 挖空，结果写到 layer 8。

---

## 下一周预告

下一周：[第 15 周 — `string` 全家桶](../15/lesson_zh.md)（Catalog A）。总表：[docs/COVERAGE.md](../../docs/COVERAGE.md)。

---

## 给家长 / 老师

选修周。成功标准：`make week28-10` 写出 `tmp/week28_poster.gds` 与 `tmp/week28_report.txt`。用 calibredrv。
