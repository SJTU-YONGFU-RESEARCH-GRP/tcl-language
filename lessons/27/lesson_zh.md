# 第 27 周 — 拼接版图：`layout filemerge` / `$L import layout`

> [10 周计划](../../PLAN.md) 之后的选修进阶周。  
> 目标：把两份小 GDS **拼成一套零件**——磁盘上用 `filemerge`，内存里用 `import layout`。

**环境：** Calibre DESIGNrev。帮助：[docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md)。

---

## 学习目标

1. 写出两份 cell 名不同的输入 GDS。
2. 用 `layout filemerge -in … -in … -out …` 合并。
3. 会用 `-createtop`、`-mode rename`、以及 `-infile` + `-placecell`。
4. 会调用 `$L import layout $src 0 append`，并知道 `del=1` 的意思。
5. 完成 **merge_kit**：`tmp/week27_kit.gds` + `tmp/week27_report.txt`。

---

## 大图景

| 工具 | 作用范围 | 比喻 |
|------|----------|------|
| `layout filemerge` | 磁盘文件 | 两本图画册订成一本 |
| `$L import layout` | 内存句柄 | 把一盘乐高倒进另一盘 |
| `layout copy` | 内存 | 先复印再大胆改 |

---

## 先修

- 第 8–10 周：cell、多边形、GDS
- 第 11–12 周：iterator / ref（方便检查结果）
- Calibre：`./scripts/run_calibre_tcl.sh`

---

## 概念 1 — 两份输入

cell 名不同（如 `LEFT` / `RIGHT`），第一次合并最轻松。

见 `01_build_two_gds.tcl`。

---

## 概念 2 — 基础 `filemerge`

```tcl
layout filemerge -in left.gds -in right.gds -out merged.gds
```

- 必须写 `-in` / `-out`（光写文件名会报 Unknown option）。
- 打开结果：`layout create merged.gds -dt_expand`，再看 `$M cells`。

见 `02_filemerge_usage.tcl`、`03_filemerge_basic.tcl`。

---

## 概念 3 — `-createtop` 与重名策略

```tcl
layout filemerge -in a.gds -in b.gds -out out.gds -createtop CHIP
layout filemerge -in t1.gds -in t2.gds -out out.gds -mode rename
```

| 旗标 | 意思 |
|------|------|
| `-createtop CHIP` | 新建顶层；子 cell 挂在下面 |
| `-mode append` | 同名 → 图形合并 |
| `-mode overwrite` | 同名 → 保留后来的 |
| `-mode rename` | 同名 → 改名（如 `TOP_WB1`） |

不要同时写 `-mode rename` 和单独的 `-overwrite` 旗标——会报 “specify only one mode”。

见 `04_createtop.tcl`、`05_mode_rename.tcl`。

---

## 概念 4 — 合并时按坐标放置

```tcl
layout filemerge \
    -infile {-name left.gds  -placecell {-refcell LEFT  -x 0  -y 0}} \
    -infile {-name right.gds -placecell {-refcell RIGHT -x 50 -y 0}} \
    -out placed.gds \
    -createtop CHIP
```

`CHIP` 下会出现你指定坐标的 ref。

见 `06_placecell.tcl`。

---

## 概念 5 — `$L import layout`

本机可用写法：

```tcl
$L import layout $src 0 append
#                 ^句柄   ^del  ^mode
```

| 参数 | 取值 | 含义 |
|------|------|------|
| `$src` | layout 句柄 | 从哪里吸进来 |
| `$del` | `0` 或 `1` | `0` 保留源；`1` 吸完删掉源句柄 |
| `$mode` | `append` / `overwrite` / `rename` | 同名 cell 怎么处理 |

参数不对会打印 Usage；把 mode 写成数字会提示 valid modes。

见 `07_import_layout.tcl`、`08_import_del_modes.tcl`、`11_import_usage_hint.tcl`。

---

## 概念 6 — `layout copy`（帮手）

```tcl
set dup [layout copy $src]
```

内存复印。见 `09_layout_copy.tcl`。

---

## 每日练习

| 天 | 目标 | 文件 |
|----|------|------|
| 1 | 两份 GDS | `01`、`02` |
| 2 | 基础 filemerge | `03` |
| 3 | createtop / rename / placecell | `04`、`05`、`06` |
| 4 | import layout | `07`、`08`、`11` |
| 5 | **merge_kit** | `10` |

### 检查清单

- [ ] `-in` / `-out` filemerge  
- [ ] `-createtop` / `-mode rename`  
- [ ] `-infile` + `-placecell`  
- [ ] `import layout` 的 `del` + `mode`  
- [ ] 写出 kit GDS + 报告  

---

## 常见错误

| 现象 | 改法 |
|------|------|
| `Unknown option file.gds` | 写成 `-in file.gds` |
| `Please specify only one mode` | 只用 `-mode rename` **或** `-overwrite` 之一 |
| `valid modes = {append,…}` | 第三个参数必须是模式**名字**，不能是 `0` |
| 源句柄没了 | 用了 `del=1` — 重新打开 GDS，或改用 `del=0` |

---

## 示例脚本

```bash
make week27-01
make week27
make week27-10
```

| # | 文件 | 重点 |
|---|------|------|
| 01 | `01_build_two_gds.tcl` | 输入 |
| 02 | `02_filemerge_usage.tcl` | Usage |
| 03 | `03_filemerge_basic.tcl` | 基础合并 |
| 04 | `04_createtop.tcl` | `-createtop` |
| 05 | `05_mode_rename.tcl` | `-mode rename` |
| 06 | `06_placecell.tcl` | 按坐标拼接 |
| 07 | `07_import_layout.tcl` | import 基础 |
| 08 | `08_import_del_modes.tcl` | del + 模式 |
| 09 | `09_layout_copy.tcl` | `layout copy` |
| 10 | `10_merge_kit.tcl` | **本周小作品** |
| 11 | `11_import_usage_hint.tcl` | 参数错误 |
| 12 | `12_run_checklist.tcl` | 检查清单 |

---

## 挑战题

用 `-placecell` 把三块放在 `(0,0)`、`(40,0)`、`(0,40)`，顶层叫 `CITY`，再用 `iterator ref` 打印全部引用。

---

## 下一周预告

下一选修周：[第 14 周 — AND / OR / NOT / SIZE](../14/lesson_zh.md)。再往后：RDB、GUI 宏。

---

## 给家长 / 老师

选修周。成功标准：`make week27-10` 写出 `tmp/week27_kit.gds` 和简短报告。用 calibredrv。
