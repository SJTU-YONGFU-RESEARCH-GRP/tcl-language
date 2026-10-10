# 第 11 周 — 遍历图形：`$L iterator`（poly / wire / text）

> 可选进阶周，接在 [10 周计划](../../PLAN.md) 之后。  
> 目标：把某个 cell、某层上的 polygon / wire / text **一个个列出来**——不只问「有没有层」，还问「画了什么」。

**环境：** Calibre DESIGNrev。帮助：[docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md)。

---

## 学习目标

1. 会调用 `$L iterator poly TOP 1 range 0 end`，得到坐标组列表。
2. 同样方式遍历 `wire`、`text`。
3. 用 `foreach` 打印每个图形。
4. 能说明：`$L layers` = 清单；`iterator` = 某一层上的细节。
5. 完成 **dump_shapes**：把图形摘要写到 `tmp/week11_dump.txt`。

---

## 大想法

| 第 9 周 | 第 11 周 |
|---------|----------|
| 「有哪些房间 / 彩纸？」 | 「这张彩纸上画了什么？」 |
| `$L layers` → `1 2` | iterator → 每个多边形的坐标 |

比喻：第 9 周数有几张彩纸；第 11 周读第 1 张纸上的每一笔涂鸦。

---

## 概念 1 — 语法（来自 Calibre Usage）

```
$L iterator {wire|poly|text} <cell> <list of layers> range <l> <h> ...
```

本机可用写法：

```tcl
set polys [$L iterator poly TOP 1 range 0 end]
set wires [$L iterator wire TOP 2 range 0 end]
set texts [$L iterator text TOP 1 range 0 end]
```

- `range 0 end` 表示从第一个到最后一个。
- 层号写成 `1` 或 `{1}` 都可以。

见 `02_iterator_usage_hint.tcl`、`03_iterator_poly.tcl`。

---

## 概念 2 — `foreach` 遍历结果

```tcl
foreach p $polys {
    puts "coords = $p"
}
```

每个 `$p` 是一个图形的数据（坐标或文字内容）。

见 `04_foreach_poly.tcl`。

---

## 概念 3 — 清单 vs 细节

```tcl
puts [$L layers]                          ;# 有哪些层
set n [llength [$L iterator poly TOP 1 range 0 end]]  ;# 第 1 层有几个 polygon
```

见 `07_layers_vs_iterator.tcl`。

---

## 每日练习

| 天 | 目标 | 文件 |
|----|------|------|
| 1 | 建样例 + poly | `01`、`02`、`03` |
| 2 | wire + text | `05`、`06` |
| 3 | foreach + 计数 | `04`、`08` |
| 4 | 对比第 9 周 | `07`、`09` |
| 5 | **dump_shapes** | `10` |

### 检查清单

- [ ] iterator poly  
- [ ] iterator wire / text  
- [ ] foreach 打印  
- [ ] layers vs iterator  
- [ ] 完成 dump_shapes  

---

## 常见错误

| 现象 | 怎么办 |
|------|--------|
| `Not enough arguments` | 需要 cell + layer + `range lo hi` |
| 没有 week11_shapes.gds | 先 `make week11-01` |
| 某层结果为空 | 层号不对 — 先看 `$L layers` |

---

## 示例脚本

```bash
make week11-01
make week11
make week11-10
```

| 编号 | 文件 | 重点 |
|------|------|------|
| 01 | `01_build_sample_shapes.tcl` | 样例 GDS |
| 02 | `02_iterator_usage_hint.tcl` | Usage |
| 03 | `03_iterator_poly.tcl` | poly |
| 04 | `04_foreach_poly.tcl` | foreach |
| 05 | `05_iterator_wire.tcl` | wire |
| 06 | `06_iterator_text.tcl` | text |
| 07 | `07_layers_vs_iterator.tcl` | 对比 |
| 08 | `08_count_all_shapes.tcl` | 统计 |
| 09 | `09_iterator_on_week8_gds.tcl` | 旧作业 |
| 10 | `10_dump_shapes.tcl` | **作品** |
| 11 | `11_iterator_ref_bonus.tcl` | ref 加分 |
| 12 | `12_run_checklist.tcl` | 清单 |

---

## 下一站

PLAN 附录：`flatten` / `expand ref`、`filemerge`、布尔运算、RDB、GUI 宏。

---

## 给家长 / 老师

可选周。成功：孩子跑通 `make week11-10`，并打开 `tmp/week11_dump.txt` 看摘要。
