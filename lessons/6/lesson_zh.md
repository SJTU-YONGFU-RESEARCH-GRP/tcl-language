# 第 6 周 — 字符串全家桶：`string`

> 属于 [PLAN.md](../../PLAN.md) **M10**（第 1–10 周）。  
> 目标：掌握 `string` 集合命令 — 长度、切片、大小写、去空格、查找、替换。  
> 覆盖表：[docs/COVERAGE.md](../../docs/COVERAGE.md)。

**环境：** 普通 `tclsh`（`make week6`）。

---

## 学习目标

1. 用 `length` / `index` / `range` 量与切。
2. 改大小写、去空格。
3. 用 `first` / `last` / `match` / `equal` / `compare` 查找比较。
4. 用 `map` / `replace` / `repeat` / `reverse` / `cat` 变换。
5. 完成 **string_toolkit**：整理一行乱字 → `tmp/week6_toolkit.txt`。

---

## 大图景

| 生活 | Tcl |
|------|-----|
| 数字母 | `string length` |
| 剪一段 | `string range` |
| 变大写 | `string toupper` |
| 去掉边空格 | `string trim` |
| 找字母 | `string first` |
| 换词 | `string map` |

---

## 先修

第 1–5 周（`puts`、`set`、列表、条件、`proc`）。本周起继续加深 Tcl 语法（M10）。

---

## 概念 1 — 长度、下标、切片

```tcl
string length "Hello"
string index  "ABC" 0
string range  "ABCDEF" 1 3
```

见 `01_string_length.tcl`、`02_index_range.tcl`。

---

## 概念 2 — 大小写与 trim

```tcl
string tolower "Hi"
string toupper "Hi"
string totitle "hello world"
string trim "  x  "
```

见 `03_case.tcl`、`04_trim.tcl`。

---

## 概念 3 — 查找与比较

```tcl
string first a banana
string match ban* banana
string equal a a
string compare a b
```

`first`/`last` 返回 `-1` 表示没找到。

见 `05_find_match.tcl`。

---

## 概念 4 — map / replace / repeat / reverse / cat

见 `06_map_replace.tcl`、`07_repeat_reverse_cat.tcl`。

---

## 概念 5 — `string is` 与发现子命令

```tcl
string is integer -strict 42
dict keys [namespace ensemble configure string -map]
```

见 `08`、`09`、`11`。

---

## 每日练习

| 天 | 目标 | 文件 |
|----|------|------|
| 1 | length / index / range | `01`、`02` |
| 2 | case / trim | `03`、`04` |
| 3 | find / match | `05` |
| 4 | map / 变换 | `06`、`07` |
| 5 | **string_toolkit** | `10` |

### 检查清单

- [ ] length / index / range  
- [ ] case + trim  
- [ ] first / match / equal  
- [ ] map / replace  
- [ ] 写出 toolkit 报告  

---

## 常见错误

| 现象 | 改法 |
|------|------|
| `first` 得到 `-1` | 子串不存在，检查拼写/大小写 |
| `match` 总是 0 | 用 glob 的 `*`/`?`，不是正则（正则在第 22 周） |
| trim 没效果 | 要去掉的不是空格时，传入字符集合 |

---

## 示例脚本

```bash
make week6-01
make week6
make week6-10
```

---

## 挑战题

写 `proc slugify s`：trim → 小写 → 空格换成 `_`。

---

## 下一周预告

第 16 周 — 列表进阶（`lsearch` `lsort` `lmap` …）。

---

## 给家长 / 老师

M10 用 **tclsh**。成功标准：`make week6-10` 写出 `tmp/week6_toolkit.txt`。下周预告：第 7 周列表进阶。
