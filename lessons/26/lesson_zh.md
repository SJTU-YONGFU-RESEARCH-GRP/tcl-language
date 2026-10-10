# 第 26 周 — 层次展开：`$L flatten` / `expand ref`

> [10 周计划](../../PLAN.md) 之后的选修进阶周。  
> 目标：把「引用别的 cell」变成「本 cell 上真正的多边形」。

**环境：** Calibre DESIGNrev。帮助：[docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md)。

---

## 学习目标

1. 建小层次：BOX 里有多边形；TOP 里用 `create ref` 放两个实例。
2. 跑 `$L flatten cell TOP`，看到 ref 消失、TOP 上出现多边形。
3. 使用 `-withDelete`，观察不再被用的子 cell 从 `$L cells` 消失。
4. 用 `$L expand ref`（或 `flatten ref`）只展开**某一个**实例（参数要和放置一致）。
5. 完成 **flatten_report**：把展开前后写进 `tmp/week26_report.txt`。

---

## 大图景

| 第 10 周 | 第 26 周 |
|----------|----------|
| 盖章（`create ref`） | 把章「揭」成纸上的真墨迹 |
| 层次还在 | Flatten = 一张平铺大图 |

生活比喻：乐高说明书里写「用某某零件盒」。**Flatten** 是把所有砖块轮廓画到一张大纸上；**只 expand 一个 ref** 是只拆开桌上某一位置的那一盒。

---

## 先修

- 第 8 周：`create cell` / `create layer` / `create polygon`
- 第 10 周：`create ref`
- 第 11 周：`iterator poly` / `iterator ref`（方便对比前后）
- Calibre：`./scripts/run_calibre_tcl.sh`（家长/老师先跑 `./scripts/setup_calibredrv.sh`）

---

## 概念 1 — 展开前的层次

```tcl
$L create cell BOX
$L create polygon BOX 1_0 0 0 10 10
$L create cell TOP
$L create ref TOP BOX 0 0 0 0 1
$L create ref TOP BOX 20 0 0 0 1
```

典型快照：

| 查询 | 展开前 |
|------|--------|
| `$L children TOP` | `BOX` |
| `iterator ref TOP` | 2 个 ref |
| `iterator poly TOP 1 …` | 0 |
| `iterator poly BOX 1 …` | 1 |

见 `01_build_hierarchy.tcl`、`03_before_snapshot.tcl`。

---

## 概念 2 — `$L flatten cell TOP`

```tcl
$L flatten cell TOP
```

Usage（Calibre）：`flatten cell <cellname> [-withDelete]`。

展开后（不加 `-withDelete`）：

- TOP 上的 ref → 没了
- TOP 上的多边形 → 通常 **2** 个（每个原实例一个，坐标随放置平移）
- `BOX` 可能仍在 `$L cells` 里

坐标直觉：

```
{0 0 10 0 10 10 0 10}     ;# 放在 (0,0)
{20 0 30 0 30 10 20 10}    ;# 放在 (20,0)
```

见 `04_flatten_cell.tcl`、`09_coords_after_flatten.tcl`。

---

## 概念 3 — `-withDelete`

```tcl
$L flatten cell TOP -withDelete
```

先展开，再删掉没人引用的子 cell。常见结果：`$L cells` 只剩 `TOP`。

见 `05_with_delete.tcl`。

---

## 概念 4 — 只拆一个：`expand ref` / `flatten ref`

必须**先有**匹配的 `create ref`，然后：

```tcl
$L expand ref TOP BOX 0 0 0 0 1
# 参数与 create ref 一致：父 cell、子 cell、x y mirror angle mag
```

- 只展开那一个实例
- 其他 ref 还在
- 本机上同参数的 `flatten ref …` 效果相同

若找不到匹配的 sref，Calibre 会报错——先 `create ref`（见 `11_need_existing_ref.tcl`）。

见 `06_expand_one_ref.tcl`、`07_flatten_ref_same.tcl`、`08_compare_cell_vs_ref.tcl`。

---

## 概念 5 — Usage 提示

参数不全时会打印 Usage：

```tcl
catch {$L flatten} msg   ;# layoutN flatten <cell|ref|aref> ...
catch {$L expand} msg    ;# layoutN expand <cell|ref> ...
```

见 `02_flatten_usage_hint.tcl`。

---

## 每日练习

| 天 | 目标 | 文件 |
|----|------|------|
| 1 | 建层次 + 展开前快照 | `01`、`02`、`03` |
| 2 | `flatten cell` | `04`、`09` |
| 3 | `-withDelete` | `05` |
| 4 | 单个 expand / flatten ref | `06`、`07`、`08` |
| 5 | **flatten_report** | `10` |

### 检查清单

- [ ] 能建 BOX + TOP 的 ref  
- [ ] 会 `flatten cell TOP`  
- [ ] 知道 `-withDelete`  
- [ ] 会按放置参数 expand/flatten 一个 ref  
- [ ] 写出 `tmp/week26_report.txt`  

---

## 常见错误

| 现象 | 原因 | 改法 |
|------|------|------|
| `unable to expand ref` | 没有匹配的 `create ref` | 先用相同 x/y/mirror/angle/mag 创建 ref |
| TOP 上仍是 0 个多边形 | 忘了 flatten / cell 名错了 | `flatten cell TOP` 再 `iterator poly` |
| `cells` 里还有 `BOX` | 没加 `-withDelete` | 需要清掉时加上 |
| `Unrecognized type arg (TOP)` | 写成了 `flatten TOP` | 要用 `flatten cell TOP` |

---

## 示例脚本

```bash
make week26-01
make week26
make week26-10
```

| # | 文件 | 重点 |
|---|------|------|
| 01 | `01_build_hierarchy.tcl` | BOX + 两个 ref → GDS |
| 02 | `02_flatten_usage_hint.tcl` | Usage 提示 |
| 03 | `03_before_snapshot.tcl` | 展开前清单 |
| 04 | `04_flatten_cell.tcl` | `flatten cell` |
| 05 | `05_with_delete.tcl` | `-withDelete` |
| 06 | `06_expand_one_ref.tcl` | 单个 `expand ref` |
| 07 | `07_flatten_ref_same.tcl` | 与 `flatten ref` 对照 |
| 08 | `08_compare_cell_vs_ref.tcl` | 整 cell vs 单个 |
| 09 | `09_coords_after_flatten.tcl` | 平移后的坐标 |
| 10 | `10_flatten_report.tcl` | **本周小作品** |
| 11 | `11_need_existing_ref.tcl` | 没有 ref 就报错 |
| 12 | `12_run_checklist.tcl` | 检查清单 |

---

## 挑战题

再放第三个 ref 在 `(0,20)`，只用 `expand ref` 展开它，另外两个仍是 ref，打印剩下的 `iterator ref`。

---

## 下一周预告

下一选修周：[第 13 周 — filemerge / import layout](../13/lesson_zh.md)。再往后：布尔运算（`AND`/`OR`/`NOT`/`SIZE`）、RDB、GUI 宏。

---

## 给家长 / 老师

选修周。成功标准：孩子跑通 `make week26-10`，打开 `tmp/week26_report.txt`，前后数量说得通。用 calibredrv，不要用裸 `tclsh`。
