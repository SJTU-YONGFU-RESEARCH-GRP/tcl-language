#!/usr/bin/env python3
"""Generate multi-language MkDocs site content using mkdocs-static-i18n.

Features:
- English as default language at root (/)
- Clean language switcher (English <-> 简体中文 at /zh/)
- FanqinZeng signature academic palette:
    --paper: #f7f6f0; --ink: #253934; --teal: #17776b; --orange: #b96b28; --code: #1d302d
- WebAssembly Tcl 8.6 interactive workshop and runner
- 18 real-world data exercises and solutions (54 tasks)
- 6 capstone data engineering projects (A–F)
- GateUltra homework hub & thy031 quizzes
- Pure-Tcl DRV-Lite layout simulator and STA timing analyzer lab
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "lessons"
WEBSITE = ROOT / "website"
DOCS = WEBSITE / "docs"
GITHUB = "https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language"

LEGACY_WEEK_MAP = {
    7: 21,
    8: 22,
    9: 23,
    10: 24,
    11: 25,
    12: 26,
    13: 27,
    14: 28,
}


def week_dirs() -> list[Path]:
    weeks = []
    for p in LESSONS.iterdir():
        if not p.is_dir() or not p.name.isdigit():
            continue
        if (p / "lesson_en.md").is_file() and (p / "lesson_zh.md").is_file():
            weeks.append(p)
    return sorted(weeks, key=lambda p: int(p.name))


def first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"


def short_title(heading: str, week: int) -> str:
    patterns = [
        rf"^Week\s+{week}\s*[—–\-:]\s*",
        rf"^第\s*{week}\s*周\s*[—–\-:]\s*",
    ]
    out = heading
    for pat in patterns:
        out = re.sub(pat, "", out, count=1, flags=re.IGNORECASE)
    return out.strip() or heading


def rewrite_lesson_links(md: str) -> str:
    md = re.sub(r"\]\(\.\./\.\./PLAN\.md\)", f"]({GITHUB}/blob/main/PLAN.md)", md)
    md = re.sub(r"\]\(\.\./PLAN\.md\)", f"]({GITHUB}/blob/main/PLAN.md)", md)

    md = md.replace("](../../docs/TCL_HELP.md)", "](../../help/tcl.md)")
    md = md.replace("](../../docs/CALIBRE_HELP.md)", "](../../help/calibre.md)")
    md = md.replace("](../../docs/COVERAGE.md)", "](../../help/coverage.md)")
    md = md.replace("](../help/calibre.md)", "](../../help/calibre.md)")
    md = md.replace("](../help/coverage.md)", "](../../help/coverage.md)")
    md = md.replace("](../help/tcl.md)", "](../../help/tcl.md)")

    existing = {int(p.name) for p in week_dirs()}

    def sibling_lesson(m: re.Match[str]) -> str:
        other = int(m.group(1))
        target = other
        if target not in existing:
            target = LEGACY_WEEK_MAP.get(other, other)
        if target in existing:
            return f"](../week{target}/index.md)"
        return f"]({GITHUB}/blob/main/lessons/{other}/lesson_en.md)"

    md = re.sub(
        r"\]\(\.\./(\d+)/lesson_(en|zh)\.md\)",
        sibling_lesson,
        md,
    )

    md = md.replace("](../README.md)", "](../../index.md)")
    return md


def rewrite_help_links(md: str, name: str) -> str:
    md = re.sub(r"\]\(\.\./PLAN\.md\)", f"]({GITHUB}/blob/main/PLAN.md)", md)
    md = md.replace("](COVERAGE.md)", "](coverage.md)")
    md = md.replace("](CALIBRE_HELP.md)", "](calibre.md)")
    md = md.replace("](TCL_HELP.md)", "](tcl.md)")
    md = md.replace("](TIMING_ANALYZER_LAB.md)", "](timing_lab.md)")
    md = md.replace("](DRVLITE_HELP.md)", "](drvlite.md)")
    md = re.sub(
        r"\]\(\.\./examples/([^)]+)\)",
        rf"]({GITHUB}/blob/main/examples/\1)",
        md,
    )
    md = re.sub(
        r"\]\(\.\./lessons/(\d+)/\)",
        r"](../lessons/week\1/index.md)",
        md,
    )
    md = re.sub(
        r"\]\(\.\./lessons/README\.md\)",
        r"](../index.md)",
        md,
    )
    md = re.sub(
        r"\[([^\]]+)\]\(\.\./lessons/STUDY_GUIDE_[^)]+\)",
        r"\1",
        md,
    )
    md = re.sub(
        r"\[([^\]]+)\]\(\.\./en/STUDY_GUIDE_[^)]+\)",
        r"\1",
        md,
    )
    md = md.replace("](../en/README.md)", "](../index.md)")
    md = md.replace("](../en/)", "](../index.md)")
    md = re.sub(r"\]\(\.\./en/(\d+)/\)", r"](../lessons/week\1/index.md)", md)
    md = re.sub(r"\]\(\.\./zh/(\d+)/\)", r"](../lessons/week\1/index.md)", md)
    md = re.sub(
        r"\]\(\.\./lessons/?\)",
        r"](../index.md)",
        md,
    )
    md = re.sub(
        r"\]\(\.\./lessons\)",
        r"](../index.md)",
        md,
    )
    return md


def examples_page(week_dir: Path, week: int, lang: str) -> str:
    tcl_files = sorted(week_dir.glob("*.tcl"))
    if lang == "zh":
        lines = [
            f"# 第 {week} 周 — 示例脚本",
            "",
            f"可在本地仓库运行：`make week{week}-NN`（见 [首页](../../index.md)）。",
            "",
        ]
    else:
        lines = [
            f"# Week {week} — Example Scripts",
            "",
            f"Run locally with `make week{week}-NN` (see [Home](../../index.md)).",
            "",
        ]
    if not tcl_files:
        lines.append("_No `.tcl` files in this week yet._")
        return "\n".join(lines) + "\n"

    for path in tcl_files:
        blob = f"{GITHUB}/blob/main/lessons/{week}/{path.name}"
        lines.append(f"## `{path.name}`")
        lines.append("")
        lines.append(f"[View on GitHub]({blob})")
        lines.append("")
        lines.append("```tcl")
        lines.append(path.read_text(encoding="utf-8").rstrip())
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def copy_workshop() -> None:
    src = WEBSITE / "workshop"
    dst = DOCS / "wasm-lab"
    if src.exists():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f"Copied standalone WASM workshop -> {dst}")


def copy_assets() -> None:
    src = WEBSITE / "assets"
    dst = DOCS / "assets"
    if src.exists():
        if not dst.exists():
            dst.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            target = dst / item.name
            if item.is_dir():
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(item, target)
            else:
                shutil.copy2(item, target)
        print(f"Copied website assets -> {dst}")


def copy_help_docs() -> None:
    help_dir = DOCS / "help"
    help_dir.mkdir(parents=True, exist_ok=True)
    mapping = {
        "TCL_HELP.md": "tcl.md",
        "CALIBRE_HELP.md": "calibre.md",
        "COVERAGE.md": "coverage.md",
        "TIMING_ANALYZER_LAB.md": "timing_lab.md",
        "DRVLITE_HELP.md": "drvlite.md",
    }
    for src_name, dst_name in mapping.items():
        src = ROOT / "docs" / src_name
        if src.is_file():
            text = rewrite_help_links(src.read_text(encoding="utf-8"), src_name)
            (help_dir / dst_name).write_text(text, encoding="utf-8")
            # Create Chinese sibling file (.zh.md)
            zh_name = dst_name.replace(".md", ".zh.md")
            (help_dir / zh_name).write_text(text, encoding="utf-8")


def write_contributors_pages() -> None:
    src = ROOT / "CONTRIBUTORS.md"
    if not src.is_file():
        return
    text = src.read_text(encoding="utf-8")
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)
    body = "\n".join(lines).rstrip() + "\n"
    
    en_page = (
        "# Contributors & Attribution\n\n"
        f"Course collaborators and student project contributors. Source: "
        f"[`CONTRIBUTORS.md`]({GITHUB}/blob/main/CONTRIBUTORS.md) "
        f"on GitHub.\n\n"
        f"{body}"
    )
    (DOCS / "contributors.md").write_text(en_page, encoding="utf-8")

    zh_page = (
        "# 贡献者与致谢名录\n\n"
        f"课程核心团队与优秀学生项目贡献者。GitHub 源码： "
        f"[`CONTRIBUTORS.md`]({GITHUB}/blob/main/CONTRIBUTORS.md)。\n\n"
        f"{body}"
    )
    (DOCS / "contributors.zh.md").write_text(zh_page, encoding="utf-8")


def write_workshop_pages() -> None:
    en_content = f"""# 🚀 Interactive Tcl Workshop (WASM)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">WASM Tcl 8.6.6</span>
  <span class="tcl-badge amber">100% In-Browser Sandbox</span>
  <span class="tcl-badge">Zero Installation</span>
  <span class="tcl-badge amber">Created by FanqinZeng</span>
</div>

A native Tcl 8.6.6 execution environment compiled to WebAssembly, featuring 18 guided exercises (54 hands-on tasks), 6 industrial data projects, and visual memory/variable inspector panels.

<div class="tcl-cta-group" style="margin: 20px 0 28px;">
  <a href="../wasm-lab/" target="_blank" class="tcl-btn tcl-btn-primary" style="font-size: 15px; padding: 12px 24px;">
    🚀 Launch Fullscreen Workshop ↗
  </a>
  <a href="../exercises/" class="tcl-btn tcl-btn-secondary" style="font-size: 15px; padding: 12px 24px;">
    🎯 Explore 18 Exercises & Solutions →
  </a>
  <a href="../capstone/" class="tcl-btn tcl-btn-secondary" style="font-size: 15px; padding: 12px 24px;">
    🏆 Explore 6 Capstone Projects →
  </a>
</div>

---

## 🛠️ Key Architectural Highlights

<div class="tcl-pillars">
  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">⚡</div>
    <div class="tcl-pillar-title">Client-Side WebAssembly Runtime</div>
    <div class="tcl-pillar-desc">
      Powered by WACL (WebAssembly Tcl 8.6.6). Code executes locally inside browser memory sandbox with zero server latency or network roundtrips.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🧪</div>
    <div class="tcl-pillar-title">18 Graded Labs & Auto-Testing</div>
    <div class="tcl-pillar-desc">
      From basic substitutions to regex, nested dictionaries, and file parsing. Each lab provides starter templates, assertion criteria, and full solutions.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">📊</div>
    <div class="tcl-pillar-title">Visual Variable & Data Inspector</div>
    <div class="tcl-pillar-desc">
      Post-execution inspection renders local variables, dictionary trees, list grids, runtime events, and formatted standard output.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">💾</div>
    <div class="tcl-pillar-title">Industrial Datasets</div>
    <div class="tcl-pillar-desc">
      Bundled with authentic wafer defect logs, server telemetry, and weather data (<code>chip_runs.csv</code>, <code>wafers.csv</code>, <code>top10_servers.tsv</code>).
    </div>
  </div>
</div>

---

## 💻 Live In-Browser Laboratory

Interact directly with the embedded runner below, or launch fullscreen in a new tab:

<div style="margin-top: 20px; border: 1px solid var(--tcl-border); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.06);">
  <div style="background: var(--tcl-slate-light); padding: 12px 18px; border-bottom: 1px solid var(--tcl-border); display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
    <span><strong>Tcl WASM Interactive Lab</strong> · Powered by WebAssembly & FanqinZeng Workshop Engine</span>
    <a href="../wasm-lab/" target="_blank" style="color: var(--teal); font-weight: 600; text-decoration: none;">Launch Fullscreen ↗</a>
  </div>
  <iframe src="../wasm-lab/" style="width: 100%; height: 880px; border: 0;" title="Tcl WASM Workshop"></iframe>
</div>
"""
    (DOCS / "workshop.md").write_text(en_content, encoding="utf-8")

    zh_content = f"""# 🚀 Tcl 自动化交互工作坊 (Interactive WASM Lab)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">WASM Tcl 8.6.6</span>
  <span class="tcl-badge amber">100% In-Browser Sandbox</span>
  <span class="tcl-badge">Zero Installation</span>
  <span class="tcl-badge amber">Created by FanqinZeng</span>
</div>

基于 WebAssembly 技术构建的原生 Tcl 8.6.6 浏览器运行环境，集成 18 节阶梯课程（54 项实战任务）、6 个工业数据项目与内存可视化调试面板。

<div class="tcl-cta-group" style="margin: 20px 0 28px;">
  <a href="../wasm-lab/" target="_blank" class="tcl-btn tcl-btn-primary" style="font-size: 15px; padding: 12px 24px;">
    🚀 在新标签页全屏打开工作坊 (Launch Fullscreen Workshop) ↗
  </a>
  <a href="../exercises/" class="tcl-btn tcl-btn-secondary" style="font-size: 15px; padding: 12px 24px;">
    🎯 浏览 18 项练习与标准答案 →
  </a>
  <a href="../capstone/" class="tcl-btn tcl-btn-secondary" style="font-size: 15px; padding: 12px 24px;">
    🏆 探索 6 大综合数据项目 →
  </a>
</div>

---

## 🛠️ 四大核心功能与特性

<div class="tcl-pillars">
  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">⚡</div>
    <div class="tcl-pillar-title">纯客户端 WebAssembly 引擎</div>
    <div class="tcl-pillar-desc">
      内置编译为 WebAssembly 的原生 Tcl 8.6.6 解释器（WACL），所有代码完全在用户本地浏览器沙箱中毫秒级运行，无需任何后端服务器与网络依赖。
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🧪</div>
    <div class="tcl-pillar-title">18 节交互式课程与实时评测</div>
    <div class="tcl-pillar-desc">
      从变量置换、列表字典到正则表达式与文件流处理，每一节均包含明确问题背景、学习目标、Starter 起步代码、验证断言与参考答案。
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">📊</div>
    <div class="tcl-pillar-title">可视化变量与数据观察台</div>
    <div class="tcl-pillar-desc">
      脚本执行完毕后，观察台自动提取并渲染局部变量表、数据结构网格、列表单元图谱、执行耗时与控制台标准输出。
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">💾</div>
    <div class="tcl-pillar-title">真实工业场景工程数据集</div>
    <div class="tcl-pillar-desc">
      预置 <code>chip_runs.csv</code>、<code>top10_servers.tsv</code>、<code>weather_beijing.json</code> 等真实芯片机台与服务器运维数据，拒绝玩具代码。
    </div>
  </div>
</div>

---

## 💻 浏览器在线实验室 (Embedded Live Lab)

可以直接在下方嵌入式工作台中编写并运行 Tcl 代码，也可以点击上方按钮在新标签页中全屏使用：

<div style="margin-top: 20px; border: 1px solid var(--tcl-border); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.06);">
  <div style="background: var(--tcl-slate-light); padding: 12px 18px; border-bottom: 1px solid var(--tcl-border); display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
    <span><strong>Tcl WASM Interactive Lab</strong> · Powered by WebAssembly & FanqinZeng Workshop Engine</span>
    <a href="../wasm-lab/" target="_blank" style="color: var(--teal); font-weight: 600; text-decoration: none;">新标签页全屏打开 ↗</a>
  </div>
  <iframe src="../wasm-lab/" style="width: 100%; height: 880px; border: 0;" title="Tcl WASM Workshop"></iframe>
</div>
"""
    (DOCS / "workshop.zh.md").write_text(zh_content, encoding="utf-8")


def write_exercises_pages() -> None:
    en_content = f"""# 🎯 18 Practical Exercises (54 Coding Tasks)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">18 Interactive Modules</span>
  <span class="tcl-badge amber">54 Structured Tasks</span>
  <span class="tcl-badge">Starters & Solutions</span>
  <span class="tcl-badge amber">Source: FanqinZeng</span>
</div>

Curated from FanqinZeng's top-ranked educational project (Audit Score 98/100), this suite provides **18 modular practice units** (comprising 54 graduated tasks). Each module features authentic engineering data, starter code templates, test criteria, and verified reference solutions.

Execute them directly in our [🚀 Interactive WASM Lab](workshop.md) or clone locally to run under standard `tclsh`.

---

## 📋 Exercise Directory

| # | Topic | Key Skills & Tasks | Dataset | Starter | Solution |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **01** | `01-hello` | `puts` standard output & command dispatch | — | [`01.tcl`]({GITHUB}/blob/main/exercises/01/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/01/01.tcl) |
| **02** | `02-vars-and-puts` | Variable assignment & string concatenation | — | [`01.tcl`]({GITHUB}/blob/main/exercises/02/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/02/01.tcl) |
| **03** | `03-math-expressions` | Braced `expr`, integer & float arithmetic | — | [`01.tcl`]({GITHUB}/blob/main/exercises/03/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/03/01.tcl) |
| **04** | `04-condition-branch` | `if` / `elseif` / `else` conditional logic | — | [`01.tcl`]({GITHUB}/blob/main/exercises/04/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/04/01.tcl) |
| **05** | `05-loops-foreach-while` | Iteration with `foreach` and `while` | — | [`01.tcl`]({GITHUB}/blob/main/exercises/05/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/05/01.tcl) |
| **06** | `06-procedures` | Custom `proc` definitions, args & return | — | [`01.tcl`]({GITHUB}/blob/main/exercises/06/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/06/01.tcl) |
| **07** | `07-list-basics` | `list`, `lindex`, `llength`, `lappend` | — | [`01.tcl`]({GITHUB}/blob/main/exercises/07/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/07/01.tcl) |
| **08** | `08-list-filter-sort` | Sorting with `lsort`, filtering, reversing | `top10_servers.tsv` | [`01.tcl`]({GITHUB}/blob/main/exercises/08/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/08/01.tcl) |
| **09** | `09-dict-basics` | `dict create`, `dict get`, `dict set` | — | [`01.tcl`]({GITHUB}/blob/main/exercises/09/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/09/01.tcl) |
| **10** | `10-dict-nested` | Hierarchical configuration & chip specs | `chip_runs.csv` | [`01.tcl`]({GITHUB}/blob/main/exercises/10/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/10/01.tcl) |
| **11** | `11-string-operations` | String range, indexing, trim & replace | — | [`01.tcl`]({GITHUB}/blob/main/exercises/11/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/11/01.tcl) |
| **12** | `12-regex-matching` | Regular expressions with `regexp` | — | [`01.tcl`]({GITHUB}/blob/main/exercises/12/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/12/01.tcl) |
| **13** | `13-file-read-lines` | File stream handles, `open`, line-by-line | `sales_raw.csv` | [`01.tcl`]({GITHUB}/blob/main/exercises/13/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/13/01.tcl) |
| **14** | `14-csv-parsing` | CSV splitting, header alignment & nulls | `wafers.csv` | [`01.tcl`]({GITHUB}/blob/main/exercises/14/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/14/01.tcl) |
| **15** | `15-json-parsing` | JSON key-value extraction & serialization | `weather_beijing.json` | [`01.tcl`]({GITHUB}/blob/main/exercises/15/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/15/01.tcl) |
| **16** | `16-error-handling` | Robust scripts with `catch` & `try ... trap` | — | [`01.tcl`]({GITHUB}/blob/main/exercises/16/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/16/01.tcl) |
| **17** | `17-data-aggregation` | Multi-field grouping & yield percentage | `chip_runs.csv` | [`01.tcl`]({GITHUB}/blob/main/exercises/17/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/17/01.tcl) |
| **18** | `18-timing-report` | Industrial STA timing Slack & WNS check | `sample_timing.rpt` | [`01.tcl`]({GITHUB}/blob/main/exercises/18/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/18/01.tcl) |

---

## 💻 Local CLI Quickstart

```bash
# Run Exercise 1 Task 1
tclsh exercises/01/01.tcl

# Verify against solution
tclsh solutions/01/01.tcl
```
"""
    (DOCS / "exercises.md").write_text(en_content, encoding="utf-8")

    zh_content = f"""# 🎯 18 项真实数据实战练习 (18 Practical Exercises)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">18 个实战专题</span>
  <span class="tcl-badge amber">54 个阶梯任务</span>
  <span class="tcl-badge">起步模版与标准答案</span>
  <span class="tcl-badge amber">来源：FanqinZeng</span>
</div>

整合来自顶级优秀项目（FanqinZeng，评分 98/100）的 **18 节体系化实战练习**（共 54 个阶梯任务）。每项练习均基于真实工程与业务数据，提供起步代码模版（`exercises/NN/01.tcl`）、检验标准与参考实现（`solutions/NN/01.tcl`）。

可在 [🚀 交互工作坊 (WASM)](workshop.md) 中直接在浏览器运行，亦可在本地克隆仓库后使用标准 `tclsh` 执行。

---

## 📋 练习索引总览 (Exercise Directory)

| 编号 | 练习主题 | 涵盖知识点与核心任务 | 关联数据集 | 起步模版 | 标准答案 |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **01** | `01-hello` | `puts` 标准输出与基础命令结构 | — | [`01.tcl`]({GITHUB}/blob/main/exercises/01/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/01/01.tcl) |
| **02** | `02-vars-and-puts` | 变量定义、字符串连接与标点格式化 | — | [`01.tcl`]({GITHUB}/blob/main/exercises/02/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/02/01.tcl) |
| **03** | `03-math-expressions` | `expr` 花括号防护、浮点与整数运算 | — | [`01.tcl`]({GITHUB}/blob/main/exercises/03/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/03/01.tcl) |
| **04** | `04-condition-branch` | `if` / `elseif` / `else` 多分支判定 | — | [`01.tcl`]({GITHUB}/blob/main/exercises/04/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/04/01.tcl) |
| **05** | `05-loops-foreach-while` | `foreach` 与 `while` 迭代集合与步进 | — | [`01.tcl`]({GITHUB}/blob/main/exercises/05/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/05/01.tcl) |
| **06** | `06-procedures` | 自定义过程 `proc`、形参与返回值处理 | — | [`01.tcl`]({GITHUB}/blob/main/exercises/06/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/06/01.tcl) |
| **07** | `07-list-basics` | `list`、`lindex`、`llength`、`lappend` | — | [`01.tcl`]({GITHUB}/blob/main/exercises/07/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/07/01.tcl) |
| **08** | `08-list-filter-sort` | 列表排序 `lsort`、过滤与倒序变换 | `top10_servers.tsv` | [`01.tcl`]({GITHUB}/blob/main/exercises/08/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/08/01.tcl) |
| **09** | `09-dict-basics` | 字典 `dict create`、`dict get`、`dict set` | — | [`01.tcl`]({GITHUB}/blob/main/exercises/09/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/09/01.tcl) |
| **10** | `10-dict-nested` | 嵌套字典建模复杂配置与芯片规格 | `chip_runs.csv` | [`01.tcl`]({GITHUB}/blob/main/exercises/10/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/10/01.tcl) |
| **11** | `11-string-operations` | 字符串截取、匹配、替换与修剪 | — | [`01.tcl`]({GITHUB}/blob/main/exercises/11/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/11/01.tcl) |
| **12** | `12-regex-matching` | 正则表达式 `regexp` 提取关键字与数值 | — | [`01.tcl`]({GITHUB}/blob/main/exercises/12/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/12/01.tcl) |
| **13** | `13-file-read-lines` | 文件流句柄 `open`、`gets`、逐行解析 | `sales_raw.csv` | [`01.tcl`]({GITHUB}/blob/main/exercises/13/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/13/01.tcl) |
| **14** | `14-csv-parsing` | CSV 表格分割、表头对齐与空值填补 | `wafers.csv` | [`01.tcl`]({GITHUB}/blob/main/exercises/14/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/14/01.tcl) |
| **15** | `15-json-parsing` | JSON 结构化数据提取与属性转换 | `weather_beijing.json` | [`01.tcl`]({GITHUB}/blob/main/exercises/15/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/15/01.tcl) |
| **16** | `16-error-handling` | `catch` 与 `try ... trap ... finally` 健壮性 | — | [`01.tcl`]({GITHUB}/blob/main/exercises/16/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/16/01.tcl) |
| **17** | `17-data-aggregation` | 多字段分组统计、良率计算与汇总表 | `chip_runs.csv` | [`01.tcl`]({GITHUB}/blob/main/exercises/17/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/17/01.tcl) |
| **18** | `18-timing-report` | STA 时序分析报告解析与 WNS 门禁判定 | `sample_timing.rpt` | [`01.tcl`]({GITHUB}/blob/main/exercises/18/01.tcl) | [`01.tcl`]({GITHUB}/blob/main/solutions/18/01.tcl) |
"""
    (DOCS / "exercises.zh.md").write_text(zh_content, encoding="utf-8")


def write_capstone_pages() -> None:
    en_content = f"""# 🏆 6 Capstone Data Engineering Projects

<div class="tcl-badge-cluster">
  <span class="tcl-badge">6 Comprehensive Projects</span>
  <span class="tcl-badge amber">Complete Test Suites</span>
  <span class="tcl-badge">Industrial Scenarios</span>
  <span class="tcl-badge amber">Source: FanqinZeng</span>
</div>

In addition to foundational exercises, this curriculum incorporates 6 major capstone data engineering projects (Projects A–F). Each project models real-world chip development, server administration, or enterprise data workflows, complete with automated test suites (`case-1.tcl` through `case-4.tcl`), starter templates, and reference implementations.

---

## 📁 Project Matrix

<div class="tcl-units-grid">
  <div class="tcl-unit-card">
    <span class="tcl-unit-badge">PROJECT A · Telemetry</span>
    <h3>Server Access Log Statistics & Alert Filtering</h3>
    <p>Parse Nginx/Apache logs, compute top IP frequencies, identify HTTP 4xx/5xx error anomalies, and generate structured health audit reports.</p>
    <div style="font-size: 13px; margin-top: 10px;">
      <a href="{GITHUB}/blob/main/capstone/A/README.md">View Project Spec →</a> · 
      <a href="{GITHUB}/blob/main/capstone/A/solution.tcl">Solution Source</a>
    </div>
  </div>

  <div class="tcl-unit-card">
    <span class="tcl-unit-badge">PROJECT B · Semiconductor</span>
    <h3>Wafer Yield Testing & Defect Clustering</h3>
    <p>Process <code>wafers.csv</code> telemetry streams, compute batch yield rates, calculate edge defect densities, and group Bin 9 failures into sign-off dashboards.</p>
    <div style="font-size: 13px; margin-top: 10px;">
      <a href="{GITHUB}/blob/main/capstone/B/README.md">View Project Spec →</a> · 
      <a href="{GITHUB}/blob/main/capstone/B/solution.tcl">Solution Source</a>
    </div>
  </div>

  <div class="tcl-unit-card">
    <span class="tcl-unit-badge">PROJECT C · DevOps</span>
    <h3>Git Commit Metrics & Productivity Reports</h3>
    <p>Parse Git commit logs and <code>git_metrics.json</code>, aggregate author churn, merge intervals, and hotspot file distributions.</p>
    <div style="font-size: 13px; margin-top: 10px;">
      <a href="{GITHUB}/blob/main/capstone/C/README.md">View Project Spec →</a> · 
      <a href="{GITHUB}/blob/main/capstone/C/solution.tcl">Solution Source</a>
    </div>
  </div>

  <div class="tcl-unit-card">
    <span class="tcl-unit-badge">PROJECT D · Enterprise</span>
    <h3>Multi-Table Sales & Inventory Reconciliation</h3>
    <p>Reconcile multi-source CSV transaction logs, adjust for timezones and currency conversions, handle missing lines, and generate variance audits.</p>
    <div style="font-size: 13px; margin-top: 10px;">
      <a href="{GITHUB}/blob/main/capstone/D/README.md">View Project Spec →</a> · 
      <a href="{GITHUB}/blob/main/capstone/D/solution.tcl">Solution Source</a>
    </div>
  </div>

  <div class="tcl-unit-card">
    <span class="tcl-unit-badge">PROJECT E · Data Cleaning</span>
    <h3>Multi-Source JSON/CSV ETL Pipeline</h3>
    <p>Architect configurable data cleaning pipelines with field mapping, schema type coercion, default fallback imputation, and output stream normalization.</p>
    <div style="font-size: 13px; margin-top: 10px;">
      <a href="{GITHUB}/blob/main/capstone/E/README.md">View Project Spec →</a> · 
      <a href="{GITHUB}/blob/main/capstone/E/solution.tcl">Solution Source</a>
    </div>
  </div>

  <div class="tcl-unit-card">
    <span class="tcl-unit-badge">PROJECT F · VLSI EDA</span>
    <h3>STA Timing Report Parser & Layout Sign-Off Gate</h3>
    <p>Deep physical design integration: parse critical timing paths, calculate WNS/TNS, correlate with layout polygon coordinates, and enforce sign-off closure.</p>
    <div style="font-size: 13px; margin-top: 10px;">
      <a href="{GITHUB}/blob/main/capstone/F/README.md">View Project Spec →</a> · 
      <a href="{GITHUB}/blob/main/capstone/F/solution.tcl">Solution Source</a>
    </div>
  </div>
</div>

---

## 🚀 Running Verification Test Cases

Each project root contains standalone verification tests:

```bash
# Run Project A Test Case 1
cd capstone/A
tclsh case-1.tcl

# Run reference solution
tclsh solution.tcl
```
"""
    (DOCS / "capstone.md").write_text(en_content, encoding="utf-8")

    zh_content = f"""# 🏆 6 大综合数据工程项目 (Capstone Projects)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">6 个综合数据工程项目</span>
  <span class="tcl-badge amber">完整自动化测试集</span>
  <span class="tcl-badge">工业实战场景</span>
  <span class="tcl-badge amber">来源：FanqinZeng</span>
</div>

除基础练习外，本课程还收录了 6 个大型综合数据工程 Capstone 项目（Projects A–F）。每个项目都模拟了芯片研发、服务器运维或企业业务中的真实场景，包含完整的测试用例矩阵（`case-1.tcl` 到 `case-4.tcl`）、起步模版（`starter.tcl`）与满分参考解答（`solution.tcl`）。

---

## 📁 项目目录矩阵 (Project Matrix)

<div class="tcl-units-grid">
  <div class="tcl-unit-card">
    <span class="tcl-unit-badge">PROJECT A · 运维分析</span>
    <h3>服务器日志统计与告警过滤</h3>
    <p>解析 Nginx/Apache 访问日志，统计高频 IP、HTTP 4xx/5xx 错误分布与请求响应延迟异常，输出格式化健康巡检报告。</p>
    <div style="font-size: 13px; margin-top: 10px;">
      <a href="{GITHUB}/blob/main/capstone/A/README.md">查看项目文档 →</a> · 
      <a href="{GITHUB}/blob/main/capstone/A/solution.tcl">参考源码</a>
    </div>
  </div>

  <div class="tcl-unit-card">
    <span class="tcl-unit-badge">PROJECT B · 芯片测试</span>
    <h3>晶圆测试机台良率聚合与缺陷分类</h3>
    <p>处理 <code>wafers.csv</code> 与机台测试流，计算各批次平均良率（Yield Rate）、边缘缺陷密度与 Bin 9 失效聚类，生成测试闭环看板。</p>
    <div style="font-size: 13px; margin-top: 10px;">
      <a href="{GITHUB}/blob/main/capstone/B/README.md">查看项目文档 →</a> · 
      <a href="{GITHUB}/blob/main/capstone/B/solution.tcl">参考源码</a>
    </div>
  </div>

  <div class="tcl-unit-card">
    <span class="tcl-unit-badge">PROJECT C · 敏捷研发</span>
    <h3>Git 提交历史度量与研发效能报告</h3>
    <p>解析 Git 提交日志与 <code>git_metrics.json</code>，按作者、分支与模块聚合代码变更量（Churn）、合并周期与热点文件分布。</p>
    <div style="font-size: 13px; margin-top: 10px;">
      <a href="{GITHUB}/blob/main/capstone/C/README.md">查看项目文档 →</a> · 
      <a href="{GITHUB}/blob/main/capstone/C/solution.tcl">参考源码</a>
    </div>
  </div>

  <div class="tcl-unit-card">
    <span class="tcl-unit-badge">PROJECT D · 企业系统</span>
    <h3>销售与库存多表自动化流水对账</h3>
    <p>多源 CSV 账目对齐，处理时区差异、货币单位换算与缺失条目重试，自动发现财务不平账项并输出差异清单。</p>
    <div style="font-size: 13px; margin-top: 10px;">
      <a href="{GITHUB}/blob/main/capstone/D/README.md">查看项目文档 →</a> · 
      <a href="{GITHUB}/blob/main/capstone/D/solution.tcl">参考源码</a>
    </div>
  </div>

  <div class="tcl-unit-card">
    <span class="tcl-unit-badge">PROJECT E · 数据清洗</span>
    <h3>多源 JSON/CSV 跨格式清洗与转换管道</h3>
    <p>构建可配置的数据清洗流水线，支持自定义字段映射、类型推断、缺省值填补与非法字符过滤，输出规范化数据流。</p>
    <div style="font-size: 13px; margin-top: 10px;">
      <a href="{GITHUB}/blob/main/capstone/E/README.md">查看项目文档 →</a> · 
      <a href="{GITHUB}/blob/main/capstone/E/solution.tcl">参考源码</a>
    </div>
  </div>

  <div class="tcl-unit-card">
    <span class="tcl-unit-badge">PROJECT F · EDA 进阶</span>
    <h3>EDA 时序报告与版图违规闭环门禁</h3>
    <p>深入集成 VLSI 后端设计流程，自动解析 STA 报告提取关键路径，与版图违规坐标对齐，形成自动化签核决策报告。</p>
    <div style="font-size: 13px; margin-top: 10px;">
      <a href="{GITHUB}/blob/main/capstone/F/README.md">查看项目文档 →</a> · 
      <a href="{GITHUB}/blob/main/capstone/F/solution.tcl">参考源码</a>
    </div>
  </div>
</div>
"""
    (DOCS / "capstone.zh.md").write_text(zh_content, encoding="utf-8")


def write_homework_pages() -> None:
    src = ROOT / "homework" / "README.md"
    body = ""
    if src.is_file():
        body = src.read_text(encoding="utf-8")
        body = re.sub(r"\]\((week\d+/[^)]+)\)", rf"]({GITHUB}/blob/main/homework/\1)", body)
        body = re.sub(r"\]\((\.\./[^)]+)\)", rf"]({GITHUB}/blob/main/\1)", body)
        body = body.replace("](../reports/runs/)", f"]({GITHUB}/tree/main/reports/runs/)")
        body = body.replace("](../LICENSE)", f"]({GITHUB}/blob/main/LICENSE)")
        body = body.replace("](homework/README.md)", "](homework.md)")
    else:
        body = "# Student Homework Hub\n\nHomework assignments contributed by GateUltra."
    
    (DOCS / "help" / "homework.md").write_text(body, encoding="utf-8")
    (DOCS / "help" / "homework.zh.md").write_text(body, encoding="utf-8")


def write_quiz_pages() -> None:
    en_page = f"""# Chapter Quizzes & Knowledge Checks

<div class="tcl-badge-cluster">
  <span class="tcl-badge">Chapter Quizzes</span>
  <span class="tcl-badge amber">Knowledge Checks</span>
  <span class="tcl-badge">Instant Feedback</span>
  <span class="tcl-badge amber">Source: thy031</span>
</div>

Curated from thy031's student project, this module provides rapid knowledge-check quizzes across foundational Tcl topics.

- **Mental Model Checks**: Substitution timing comparison between `set x $a` and `set x {{a}}`.
- **Evaluation Safety**: Anti-injection checks on braced `expr {{$a + $b}}` vs unquoted variants.
- **Data Structures**: List boundaries, dictionary value extraction, and nested loops.
- **Physical Design Basics**: Polygon vertex ordering, pin declarations, and Slack sign rules.

Launch the offline quiz runner locally:

```bash
cd quiz && python3 -m http.server 8082
```
"""
    (DOCS / "help" / "quiz.md").write_text(en_page, encoding="utf-8")

    zh_page = f"""# 随堂自测题库与交互答题 (Interactive Quizzes)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">章节自测题库</span>
  <span class="tcl-badge amber">快速检验</span>
  <span class="tcl-badge">即时反馈</span>
  <span class="tcl-badge amber">来源：thy031</span>
</div>

本测验模块由 thy031 同学设计与开发，包含贯穿各周次知识点的快速小测验。

- **语法心智自测**：辨析 `set x $a` 与 `set x {{a}}` 的置换时机差异。
- **求值规则测试**：严格花括号 `expr {{$a + $b}}` 与无保护 `expr $a + $b` 的安全评测。
- **数据结构实战**：列表索引边界、字典键值提取与嵌套遍历。
- **版图与时序基础**：多边形坐标表达、引脚定义与 Slack 正负判据。
"""
    (DOCS / "help" / "quiz.zh.md").write_text(zh_page, encoding="utf-8")


def write_playground_pages() -> None:
    content = """# Interactive Tcl Web Playground

Run, test, and experiment with Tcl scripts directly in your browser without local installation.

<div style="background: var(--md-code-bg-color, #1d302d); border-radius: 8px; padding: 16px; margin: 20px 0; border: 1px solid var(--tcl-border);">
  <div style="display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; align-items: center;">
    <span style="font-weight: bold; color: var(--teal);">Load Example:</span>
    <button onclick="loadSnippet('hello')" style="background: var(--tcl-slate-light); color: var(--ink); border: 1px solid var(--tcl-border); border-radius: 4px; padding: 6px 12px; cursor: pointer;">Hello puts</button>
    <button onclick="loadSnippet('subst')" style="background: var(--tcl-slate-light); color: var(--ink); border: 1px solid var(--tcl-border); border-radius: 4px; padding: 6px 12px; cursor: pointer;">Welch Mental Model</button>
    <button onclick="loadSnippet('expr')" style="background: var(--tcl-slate-light); color: var(--ink); border: 1px solid var(--tcl-border); border-radius: 4px; padding: 6px 12px; cursor: pointer;">Braced expr</button>
    <button onclick="loadSnippet('list_dict')" style="background: var(--tcl-slate-light); color: var(--ink); border: 1px solid var(--tcl-border); border-radius: 4px; padding: 6px 12px; cursor: pointer;">List & Dict</button>
    <button onclick="loadSnippet('timing')" style="background: var(--tcl-slate-light); color: var(--ink); border: 1px solid var(--tcl-border); border-radius: 4px; padding: 6px 12px; cursor: pointer;">STA Slack Parser</button>
    <button onclick="loadSnippet('drvlite')" style="background: var(--tcl-slate-light); color: var(--ink); border: 1px solid var(--tcl-border); border-radius: 4px; padding: 6px 12px; cursor: pointer;">DRV-Lite Layout</button>
  </div>

  <textarea id="tcl-code-input" style="width: 100%; height: 200px; font-family: monospace; background: var(--code); color: #e9f1ea; border: 1px solid #334c44; border-radius: 6px; padding: 12px; box-sizing: border-box; font-size: 14px; line-height: 1.5; resize: vertical; outline: none;"></textarea>

  <div style="margin-top: 10px; display: flex; gap: 10px; align-items: center;">
    <button onclick="runTclCode()" style="background: var(--teal); color: white; border: none; border-radius: 6px; padding: 8px 18px; font-weight: bold; cursor: pointer;">Run Script (Ctrl+Enter)</button>
    <button onclick="clearOutput()" style="background: transparent; color: var(--muted); border: 1px solid var(--tcl-border); border-radius: 6px; padding: 8px 14px; cursor: pointer;">Clear Output</button>
    <span id="tcl-status" style="font-size: 13px; color: var(--muted);">Ready</span>
  </div>

  <div style="margin-top: 14px;">
    <div style="font-size: 12px; color: var(--muted); margin-bottom: 4px; font-weight: bold;">Standard Output:</div>
    <pre id="tcl-output" style="background: #0f1c19; color: #a7f3d0; border-radius: 6px; padding: 12px; min-height: 80px; max-height: 250px; overflow-y: auto; font-family: monospace; font-size: 13px; margin: 0; white-space: pre-wrap;"></pre>
  </div>
</div>

<script>
const snippets = {
  hello: `# 01. Hello puts & Variables
set course "Tcl for VLSI"
set version 2.0
puts "Welcome to $course (Release $version)!"
puts "Zero install, runs directly in browser."
`,
  subst: `# 02. Brent Welch Mental Model: Grouping -> Substitution -> Invocation
set word "EDA"
# Double quotes: Substitution performed
puts "Double quotes: I study $word scripting"
# Braces: Deferred substitution (Literal)
puts {Braces prevent substitution: $word is preserved}
`,
  expr: `# 03. Safe Braced expr (Anti-Injection & Byte-Compiled)
set a 15
set b 27
set sum [expr {$a + $b}]
set ratio [expr {double($a) / $b}]
puts "Sum: $sum"
puts [format "Ratio: %.4f" $ratio]
`,
  list_dict: `# 04. Lists & Dictionaries
set layers [list M1 M2 M3 VIA1 VIA2]
puts "Available layers: $layers"
puts "Second routing layer: [lindex $layers 1]"

set cell [dict create name "INV_X1" width 1.2 height 2.4]
puts "Cell name: [dict get $cell name]"
puts "Cell area: [expr {[dict get $cell width] * [dict get $cell height]}] um^2"
`,
  timing: `# 05. Static Timing Analysis (STA) Critical Path Parser
set path_group "clk_core"
set arrival 2.45
set required 2.30
set slack [expr {$required - $arrival}]
set timing [dict create group $path_group slack $slack]

puts "Path Group: [dict get $timing group]"
puts [format "Path Slack: %.3f ns" [dict get $timing slack]]
if {$slack < 0} {
  puts ">> [GATE VIOLATION]: Timing not met, WNS degraded."
} else {
  puts ">> [TIMING MET]: Setup slack positive."
}
`,
  drvlite: `# 06. DRV-Lite Layout Object Simulation
set L [layout create]
$L create cell TOP
$L create polygon TOP 1 0 0 400 0 400 200 0 200
puts "Created cell: [$L topcell]"
puts "Cell bounding box: [$L bbox TOP]"
`
};

function loadSnippet(name) {
  const code = snippets[name];
  if (code) {
    document.getElementById('tcl-code-input').value = code;
    document.getElementById('tcl-status').innerText = 'Loaded example: ' + name;
  }
}

function clearOutput() {
  document.getElementById('tcl-output').innerText = '';
  document.getElementById('tcl-status').innerText = 'Output cleared';
}

function runTclCode() {
  const code = document.getElementById('tcl-code-input').value;
  const out = document.getElementById('tcl-output');
  const status = document.getElementById('tcl-status');
  out.innerText = '';
  status.innerText = 'Executing...';

  try {
    const lines = code.split('\\n');
    const vars = {};
    const mockLayout = { cells: {}, top: 'TOP' };

    function log(msg) {
      out.innerText += msg + '\\n';
    }

    for (let rawLine of lines) {
      let line = rawLine.trim();
      if (!line || line.startsWith('#')) continue;

      if (line.startsWith('puts ')) {
        let content = line.substring(5).trim();
        if (content.startsWith('"') && content.endsWith('"')) {
          content = content.substring(1, content.length - 1);
        } else if (content.startsWith('{') && content.endsWith('}')) {
          content = content.substring(1, content.length - 1);
          log(content);
          continue;
        }

        content = content.replace(/\\$([a-zA-Z0-9_]+)/g, (_, name) => {
          return vars[name] !== undefined ? vars[name] : '$' + name;
        });

        content = content.replace(/\\[expr\\s+([^]+)\\]/g, (_, exprStr) => {
          try {
            let sanitized = exprStr.replace(/[{}]/g, '');
            sanitized = sanitized.replace(/double\\(([^)]+)\\)/g, '$1');
            sanitized = sanitized.replace(/\\$([a-zA-Z0-9_]+)/g, (_, n) => vars[n] || 0);
            return eval(sanitized);
          } catch(e) { return '[expr error]'; }
        });

        content = content.replace(/\\[format\\s+"([^"]+)"\\s+([^]+)\\]/g, (_, fmt, val) => {
          try {
            let v = eval(val.replace(/\\$([a-zA-Z0-9_]+)/g, (_, n) => vars[n] || 0));
            return fmt.replace(/%.4f/g, v.toFixed(4)).replace(/%.3f/g, v.toFixed(3));
          } catch(e) { return val; }
        });

        content = content.replace(/\\[lindex\\s+\\$([a-zA-Z0-9_]+)\\s+(\\d+)\\]/g, (_, vName, idx) => {
          const list = vars[vName] || [];
          return Array.isArray(list) ? list[parseInt(idx)] : (list.split(' ')[parseInt(idx)] || '');
        });

        content = content.replace(/\\[dict\\s+get\\s+\\$([a-zA-Z0-9_]+)\\s+([a-zA-Z0-9_]+)\\]/g, (_, dName, kName) => {
          const d = vars[dName];
          return (d && d[kName] !== undefined) ? d[kName] : '';
        });

        content = content.replace(/\\[\\$L\\s+topcell\\]/g, () => mockLayout.top);
        content = content.replace(/\\[\\$L\\s+bbox\\s+TOP\\]/g, () => '0 0 400 200');

        log(content);
      }
      else if (line.startsWith('set ')) {
        const parts = line.split(/\\s+/);
        const varName = parts[1];
        let val = parts.slice(2).join(' ');
        if (val.startsWith('"') && val.endsWith('"')) val = val.substring(1, val.length - 1);
        else if (val.startsWith('{') && val.endsWith('}')) val = val.substring(1, val.length - 1);
        else if (val.startsWith('[layout create]')) val = 'layout0';
        else if (val.startsWith('[list ')) {
          val = val.substring(6, val.length - 1).split(' ');
        }
        else if (val.startsWith('[dict create ')) {
          let inner = val.substring(13, val.length - 1).split(' ');
          let d = {};
          for (let i = 0; i < inner.length; i += 2) {
            d[inner[i]] = inner[i+1].replace(/["']/g, '');
          }
          val = d;
        }
        else if (val.startsWith('[expr ')) {
          let inner = val.substring(6, val.length - 1).replace(/[{}]/g, '');
          inner = inner.replace(/double\\(([^)]+)\\)/g, '$1');
          inner = inner.replace(/\\$([a-zA-Z0-9_]+)/g, (_, n) => vars[n] || 0);
          try { val = eval(inner); } catch(e) { val = 0; }
        }
        vars[varName] = val;
      }
      else if (line.includes('$L create cell')) {
        const cname = line.split(/\\s+/)[3] || 'TOP';
        mockLayout.cells[cname] = true;
        mockLayout.top = cname;
      }
      else if (line.includes('$L create polygon')) {
        mockLayout.hasPoly = true;
      }
      else if (line.startsWith('if ')) {
        let condition = line.substring(3).split('{')[0].trim();
        condition = condition.replace(/[{}]/g, '');
        condition = condition.replace(/\\$([a-zA-Z0-9_]+)/g, (_, n) => vars[n] || 0);
        let branch = false;
        try { branch = eval(condition); } catch(e) {}
        if (branch && line.includes('puts ')) {
          let putPart = line.substring(line.indexOf('puts '));
          let closeIdx = putPart.indexOf('}');
          if (closeIdx !== -1) putPart = putPart.substring(0, closeIdx);
          let content = putPart.substring(5).trim().replace(/^"|"$/g, '');
          content = content.replace(/\\$([a-zA-Z0-9_]+)/g, (_, name) => vars[name]);
          log(content);
        }
      }
    }
    status.innerText = 'Finished successfully';
  } catch (err) {
    status.innerText = 'Runtime error';
    log('[Error]: ' + err.message);
  }
}

window.addEventListener('DOMContentLoaded', () => loadSnippet('hello'));
</script>

---

## Standalone WebAssembly Tcl IDE

Looking for full in-browser test grading, step-by-step interactive debugging, and memory table inspector? Launch the [🚀 Interactive Workshop (WASM)](workshop.md).
"""
    (DOCS / "playground.md").write_text(content, encoding="utf-8")
    (DOCS / "playground.zh.md").write_text(content, encoding="utf-8")


def write_stylesheets() -> None:
    css_dir = DOCS / "stylesheets"
    css_dir.mkdir(parents=True, exist_ok=True)
    css_content = """/* Custom styling for Tcl Language Lab inspired by top student educational innovations */

:root, [data-md-color-scheme="default"] {
  --paper: #f7f6f0;
  --ink: #253934;
  --muted: #64716b;
  --teal: #17776b;
  --teal-dark: #0f4f46;
  --light: #e7f2eb;
  --line: #dce1d7;
  --orange: #b96b28;
  --code: #1d302d;

  --md-default-bg-color: #f7f6f0 !important;
  --md-default-fg-color: #253934 !important;
  --md-default-fg-color--light: #64716b !important;
  --md-default-fg-color--lighter: #8b9993 !important;
  --md-primary-fg-color: #17776b !important;
  --md-primary-fg-color--light: #238b7e !important;
  --md-primary-fg-color--dark: #0f4f46 !important;
  --md-primary-bg-color: #f7f6f0 !important;
  --md-accent-fg-color: #b96b28 !important;
  --md-code-bg-color: #1d302d !important;
  --md-code-fg-color: #e9f1ea !important;

  --tcl-teal-dark: #0f4f46;
  --tcl-teal: #17776b;
  --tcl-teal-light: #e7f2eb;
  --tcl-amber: #b96b28;
  --tcl-amber-light: #fdf5ea;
  --tcl-slate-dark: #1d302d;
  --tcl-slate: #253934;
  --tcl-slate-light: #f2f0e6;
  --tcl-border: #dce1d7;
}

[data-md-color-scheme="slate"] {
  --md-default-bg-color: #13221f !important;
  --md-default-bg-color--light: #1d302d !important;
  --md-default-bg-color--lighter: #253934 !important;
  --md-default-fg-color: #f7f6f0 !important;
  --md-default-fg-color--light: #b2c2bb !important;
  --md-primary-fg-color: #238b7e !important;
  --md-primary-fg-color--dark: #17776b !important;
  --md-code-bg-color: #0f1c19 !important;
  --tcl-border: #334c44;
  --tcl-slate-light: #1d302d;
}

body, .md-typeset {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
  color: #253934;
  background-color: var(--md-default-bg-color);
}

.md-header {
  background-color: #17776b !important;
  box-shadow: 0 2px 8px rgba(15, 79, 70, 0.25) !important;
}

.md-tabs {
  background-color: #0f4f46 !important;
}

.md-tabs__link {
  font-weight: 600;
  opacity: 0.95;
}

.md-typeset h1, .md-typeset h2, .md-typeset h3 {
  font-family: Georgia, "Songti SC", "Noto Serif SC", serif;
  color: #17776b;
  letter-spacing: -0.5px;
}

[data-md-color-scheme="slate"] .md-typeset h1,
[data-md-color-scheme="slate"] .md-typeset h2,
[data-md-color-scheme="slate"] .md-typeset h3 {
  color: #4db6ac;
}

/* Hero Section */
.tcl-hero {
  padding: 30px 0 20px;
  border-bottom: 1px solid var(--tcl-border);
  margin-bottom: 24px;
}
.tcl-badge-cluster {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}
.tcl-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 600;
  background: var(--tcl-teal-light);
  color: var(--tcl-teal-dark);
  border: 1px solid rgba(23, 119, 107, 0.3);
}
[data-md-color-scheme="slate"] .tcl-badge {
  background: rgba(35, 139, 126, 0.25);
  color: #5eead4;
  border-color: rgba(94, 234, 212, 0.3);
}
.tcl-badge.amber {
  background: var(--tcl-amber-light);
  color: #b96b28;
  border-color: rgba(185, 107, 40, 0.3);
}
[data-md-color-scheme="slate"] .tcl-badge.amber {
  background: rgba(185, 107, 40, 0.2);
  color: #fcd34d;
  border-color: rgba(252, 211, 77, 0.3);
}
.tcl-hero-title {
  font-family: Georgia, "Songti SC", "Noto Serif SC", serif;
  font-size: 2.3rem;
  font-weight: 700;
  line-height: 1.25;
  margin: 8px 0 14px 0;
  color: #17776b;
}
[data-md-color-scheme="slate"] .tcl-hero-title {
  color: #5eead4;
}
.tcl-hero-subtitle {
  font-size: 1.05rem;
  line-height: 1.7;
  color: var(--md-default-fg-color--light);
  max-width: 860px;
  margin-bottom: 20px;
}
.tcl-cta-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin: 18px 0 10px;
}
.tcl-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none !important;
  transition: all 0.2s ease;
}
.tcl-btn-primary {
  background: #17776b;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(23, 119, 107, 0.25);
}
.tcl-btn-primary:hover {
  background: #0f4f46;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(23, 119, 107, 0.35);
}
.tcl-btn-secondary {
  background: var(--tcl-slate-light);
  color: var(--md-default-fg-color) !important;
  border: 1px solid var(--tcl-border);
}
.tcl-btn-secondary:hover {
  border-color: #17776b;
  background: rgba(23, 119, 107, 0.08);
  transform: translateY(-2px);
}

/* Stats Fact Strip */
.tcl-fact-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 16px;
  padding: 20px 24px;
  background: var(--tcl-slate-light);
  border: 1px solid var(--tcl-border);
  border-radius: 12px;
  margin: 24px 0 36px;
}
.tcl-fact-item {
  text-align: center;
}
.tcl-fact-val {
  font-family: Georgia, 'Songti SC', serif;
  font-size: 2rem;
  font-weight: 700;
  color: #17776b;
  display: block;
}
[data-md-color-scheme="slate"] .tcl-fact-val {
  color: #5eead4;
}
.tcl-fact-lbl {
  font-size: 0.85rem;
  color: var(--md-default-fg-color--light);
  font-weight: 500;
}

/* 3-Column Route Cards */
.tcl-routes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
  gap: 20px;
  margin: 20px 0 36px;
}
.tcl-route-card {
  padding: 24px;
  border-radius: 12px;
  border: 1px solid var(--tcl-border);
  background: var(--md-default-bg-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  position: relative;
  overflow: hidden;
  transition: all 0.25s ease;
}
.tcl-route-card:hover {
  transform: translateY(-4px);
  border-color: #17776b;
  box-shadow: 0 12px 28px rgba(23, 119, 107, 0.12);
}
.tcl-route-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: #17776b;
}
.tcl-route-card.route-exp::before { background: #b96b28; }
.tcl-route-card.route-vlsi::before { background: #0f4f46; }
.tcl-route-num {
  font-size: 12px;
  font-family: monospace;
  font-weight: 700;
  color: #17776b;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.tcl-route-card.route-exp .tcl-route-num { color: #b96b28; }
.tcl-route-card.route-vlsi .tcl-route-num { color: #0f4f46; }
.tcl-route-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 8px 0 10px;
}
.tcl-route-desc {
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--md-default-fg-color--light);
  margin-bottom: 16px;
}

/* Feature Pillars Grid */
.tcl-pillars {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
  margin: 20px 0 36px;
}
.tcl-pillar-card {
  padding: 22px;
  border-radius: 10px;
  border: 1px solid var(--tcl-border);
  background: var(--tcl-slate-light);
  transition: all 0.2s ease;
}
.tcl-pillar-card:hover {
  border-color: #17776b;
  transform: translateY(-2px);
}
.tcl-pillar-icon {
  font-size: 1.7rem;
  margin-bottom: 8px;
}
.tcl-pillar-title {
  font-size: 1.05rem;
  font-weight: 700;
  margin: 4px 0 8px;
}
.tcl-pillar-desc {
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--md-default-fg-color--light);
}

/* Unit Module Cards */
.tcl-units-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
  margin: 20px 0 30px;
}
.tcl-unit-card {
  border: 1px solid var(--tcl-border);
  border-radius: 10px;
  padding: 20px;
  background: var(--md-default-bg-color);
  transition: all 0.2s ease;
}
.tcl-unit-card:hover {
  border-color: #17776b;
  transform: translateY(-2px);
}
.tcl-unit-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(23, 119, 107, 0.12);
  color: #17776b;
  margin-bottom: 8px;
}
"""
    (css_dir / "extra.css").write_text(css_content, encoding="utf-8")


def write_home_pages(meta: list[tuple[int, str, str]]) -> None:
    en_rows = []
    zh_rows = []
    for w, en_short, zh_short in meta:
        en_rows.append(f"| Week {w:02d} | [{en_short}](lessons/week{w}/index.md) | [Examples](lessons/week{w}/examples.md) |")
        zh_rows.append(f"| 第 {w:02d} 周 | [{zh_short}](lessons/week{w}/index.md) | [示例代码](lessons/week{w}/examples.md) |")

    en_index = f"""<div class="tcl-hero">
  <div class="tcl-badge-cluster">
    <span class="tcl-badge">CC BY 4.0</span>
    <span class="tcl-badge">SJTU-YONGFU-RESEARCH-GRP</span>
    <span class="tcl-badge amber">WASM Interactive Lab</span>
    <span class="tcl-badge">DRV-Lite Simulator</span>
    <span class="tcl-badge amber">STA Timing Sign-Off</span>
    <span class="tcl-badge">Multi-Language</span>
  </div>

  <h1 class="tcl-hero-title">Tcl for VLSI · From Syntax to IC Layout & Timing Automation</h1>

  <div class="tcl-hero-subtitle">
    From foundational scripting commands to a production-grade IC physical design automation suite.<br>
    Bridging the <strong>Brent Welch 3-step evaluation mental model</strong>, <strong>in-browser WebAssembly interactive workshop</strong>, <strong>zero-license DRV-Lite layout simulator</strong>, and <strong>closed-loop STA timing sign-off</strong>.
  </div>

  <div class="tcl-cta-group">
    <a href="wasm-lab/" target="_blank" class="tcl-btn tcl-btn-primary">🚀 Launch WASM Workshop ↗</a>
    <a href="exercises/" class="tcl-btn tcl-btn-secondary">🎯 18 Practice Exercises</a>
    <a href="capstone/" class="tcl-btn tcl-btn-secondary">🏆 6 Capstone Projects</a>
    <a href="help/drvlite/" class="tcl-btn tcl-btn-secondary">📐 Layout Simulator (DRV-Lite)</a>
    <a href="help/timing_lab/" class="tcl-btn tcl-btn-secondary">⚡ Timing Analysis Lab</a>
    <a href="help/tcl/" class="tcl-btn tcl-btn-secondary">🧠 3-Step Mental Model</a>
  </div>
</div>

<div class="tcl-fact-strip">
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">40 Weeks</span>
    <span class="tcl-fact-lbl">Complete Curriculum Plan</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">18 Labs</span>
    <span class="tcl-fact-lbl">Real-World Data Exercises</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">6 Projects</span>
    <span class="tcl-fact-lbl">Capstone Data Engineering</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">100%</span>
    <span class="tcl-fact-lbl">Browser WASM Zero-Install</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">Zero License</span>
    <span class="tcl-fact-lbl">DRV-Lite Layout Simulator</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">Industrial</span>
    <span class="tcl-fact-lbl">STA Slack Sign-Off Gate</span>
  </div>
</div>

## 🎯 Recommended Learning Pathways

Choose the path tailored to your background and engineering goals:

<div class="tcl-routes">
  <div class="tcl-route-card">
    <span class="tcl-route-num">PATHWAY 01 · First Steps</span>
    <div class="tcl-route-title">New to Scripting</div>
    <div class="tcl-route-desc">
      Begin with <code>puts</code>, variables, and comments. Master the Brent Welch 3-step substitution model (Grouping $\to$ Substitution $\to$ Invocation) to demystify curly braces <code>{{}}</code> vs double quotes <code>""</code>.
    </div>
    <a href="lessons/week1/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">Start Week 1 →</a>
  </div>

  <div class="tcl-route-card route-exp">
    <span class="tcl-route-num">PATHWAY 02 · Fast Track</span>
    <div class="tcl-route-title">Experienced in Python / C</div>
    <div class="tcl-route-desc">
      Focus on Tcl's unique mechanisms: deferred substitution, braced <code>expr</code> security, list/dict manipulations, namespaces, and TclOO object-oriented design.
    </div>
    <a href="help/tcl/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">Mental Model Guide →</a>
  </div>

  <div class="tcl-route-card route-vlsi">
    <span class="tcl-route-num">PATHWAY 03 · Chip Engineering</span>
    <div class="tcl-route-title">VLSI & Physical Design</div>
    <div class="tcl-route-desc">
      Bypass EDA license bottlenecks using our pure-Tcl DRV-Lite simulator to generate polygons, wires, bounding boxes, and GDS outputs. Analyze STA timing slacks, WNS, and TNS sign-off criteria.
    </div>
    <a href="help/timing_lab/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">Timing Sign-Off Lab →</a>
  </div>
</div>

---

## 🛠️ Four Core Technological Pillars

<div class="tcl-pillars">
  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">💻</div>
    <div class="tcl-pillar-title">Client-Side WebAssembly Workshop</div>
    <div class="tcl-pillar-desc">
      Incorporating FanqinZeng's 98/100 rated platform: native Tcl 8.6.6 WebAssembly engine, 18 graduated modules, memory variable inspector, and 6 capstone projects.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">📐</div>
    <div class="tcl-pillar-title">DRV-Lite Layout Simulator</div>
    <div class="tcl-pillar-desc">
      Zero commercial EDA licenses required. Pure-Tcl layout object model implementing cell hierarchy, polygon boundaries, bounding boxes, and GDS streamout.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🧠</div>
    <div class="tcl-pillar-title">Brent Welch 3-Step Model</div>
    <div class="tcl-pillar-desc">
      Strict adherence to Argument Grouping $\to$ Value Substitution $\to$ Command Invocation, eliminating double evaluation and security hazards.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">⚡</div>
    <div class="tcl-pillar-title">Industrial STA Timing Gatekeeper</div>
    <div class="tcl-pillar-desc">
      Parse digital design timing reports, extract startpoints and endpoints, compute Worst Negative Slack (WNS) and Total Negative Slack (TNS).
    </div>
  </div>
</div>

---

## 📚 Curriculum Directory (40 Weeks)

| Week | Topic | Examples |
| :---: | :--- | :---: |
{chr(10).join(en_rows)}

---

## 🚀 Quick Start (CLI)

```bash
git clone {GITHUB}.git
cd tcl-language

make check-env        # Verify tclsh & DRV-Lite layout simulator
make drvlite-test     # Run 6 unit tests on pure-Tcl layout simulator
make timing-demo      # Run STA timing analysis lab
make week1-01         # Run Week 1 first example
make week21-01        # Run Week 21 layout script (DRV-Lite simulation)
```
"""
    (DOCS / "index.md").write_text(en_index, encoding="utf-8")

    zh_index = f"""<div class="tcl-hero">
  <div class="tcl-badge-cluster">
    <span class="tcl-badge">CC BY 4.0</span>
    <span class="tcl-badge">SJTU-YONGFU-RESEARCH-GRP</span>
    <span class="tcl-badge amber">WASM 交互工作坊</span>
    <span class="tcl-badge">DRV-Lite 版图仿真器</span>
    <span class="tcl-badge amber">STA 时序违规闭环门禁</span>
    <span class="tcl-badge">多语言支持</span>
  </div>

  <h1 class="tcl-hero-title">Tcl for VLSI · 从控制台语法到芯片版图与时序自动化</h1>

  <div class="tcl-hero-subtitle">
    从一张控制台打印卡片，到一套完整的工业级芯片版图自动化脚本与静态时序分析流水线。<br>
    结合 <strong>Brent Welch 三步置换心智模型</strong>、<strong>浏览器纯客户端 WebAssembly 交互工作坊</strong>、<strong>免商业许可 DRV-Lite 版图仿真器</strong> 与 <strong>STA 时序违规闭环门禁</strong>，让每行 Tcl 代码都能在真实工程场景中高效运行。
  </div>

  <div class="tcl-cta-group">
    <a href="wasm-lab/" target="_blank" class="tcl-btn tcl-btn-primary">🚀 交互工作坊 (WASM Lab) ↗</a>
    <a href="exercises/" class="tcl-btn tcl-btn-secondary">🎯 18 项实战练习 (Exercises)</a>
    <a href="capstone/" class="tcl-btn tcl-btn-secondary">🏆 6 大综合项目 (Capstones)</a>
    <a href="help/drvlite/" class="tcl-btn tcl-btn-secondary">📐 版图仿真器 (DRV-Lite)</a>
    <a href="help/timing_lab/" class="tcl-btn tcl-btn-secondary">⚡ 时序分析实验 (Timing Lab)</a>
    <a href="help/tcl/" class="tcl-btn tcl-btn-secondary">🧠 置换心智指南</a>
  </div>
</div>

<div class="tcl-fact-strip">
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">40 周</span>
    <span class="tcl-fact-lbl">系统进阶双语课程</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">18 项</span>
    <span class="tcl-fact-lbl">真实数据交互实战练习</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">6 个</span>
    <span class="tcl-fact-lbl">综合数据工程项目</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">100%</span>
    <span class="tcl-fact-lbl">浏览器 WASM 零安装运行</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">零授权</span>
    <span class="tcl-fact-lbl">DRV-Lite 版图仿真器</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">工业级</span>
    <span class="tcl-fact-lbl">STA 时序违规闭环门禁</span>
  </div>
</div>

## 🎯 你的学习起点：三种推荐路线

根据你的专业背景与编程经验，选择最契合的学习路径：

<div class="tcl-routes">
  <div class="tcl-route-card">
    <span class="tcl-route-num">PATHWAY 01 · 零基础启航</span>
    <div class="tcl-route-title">第一次学习编程</div>
    <div class="tcl-route-desc">
      从 <code>puts</code>、变量与注释入门。通过 Brent Welch 三步置换心智模型（切分 $\to$ 置换 $\to$ 调用），彻底理解大括号 <code>{{}}</code> 与双引号 <code>""</code> 的本质差异，告别初学者易犯的语法迷茫。
    </div>
    <a href="lessons/week1/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">从第 1 周开始 →</a>
  </div>

  <div class="tcl-route-card route-exp">
    <span class="tcl-route-num">PATHWAY 02 · 快速转栈</span>
    <div class="tcl-route-title">已有 Python / C 经验</div>
    <div class="tcl-route-desc">
      聚焦 Tcl 独特机制：大括号延迟求值、<code>expr</code> 严格花括号保护（防注入与字节编译加速）、列表与字典高效操纵、命名空间与 TclOO 面向对象设计。
    </div>
    <a href="help/tcl/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">置换心智指南 →</a>
  </div>

  <div class="tcl-route-card route-vlsi">
    <span class="tcl-route-num">PATHWAY 03 · 芯片工程</span>
    <div class="tcl-route-title">VLSI 与物理设计工程师</div>
    <div class="tcl-route-desc">
      无需商业 EDA 许可证，直接在标准 <code>tclsh</code> 下使用纯 Tcl DRV-Lite 仿真器操纵多边形、引脚与 GDS 输出；结合静态时序分析实验，解析关键路径报表，计算 WNS/TNS 闭环流片门禁。
    </div>
    <a href="help/timing_lab/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">时序分析实战 →</a>
  </div>
</div>

---

## 🛠️ 四大核心技术支柱

<div class="tcl-pillars">
  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">💻</div>
    <div class="tcl-pillar-title">纯客户端 WebAssembly 交互工作坊</div>
    <div class="tcl-pillar-desc">
      整合 FanqinZeng 98 分顶级工程创新：原生 Tcl 8.6.6 WebAssembly 运行时、18 项渐进实战、内存变量观察台与 6 大综合项目。
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">📐</div>
    <div class="tcl-pillar-title">DRV-Lite 纯 Tcl 版图仿真器</div>
    <div class="tcl-pillar-desc">
      突破 Siemens Calibre 商业许可壁垒！纯 Tcl 实现的 <code>layout</code> 对象模型，支持图纸创建、多边形绘制、边界计算与 GDS 导出。
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🧠</div>
    <div class="tcl-pillar-title">Brent Welch 3步求值心智模型</div>
    <div class="tcl-pillar-desc">
      严格遵循 Argument Grouping $\to$ Value Substitution $\to$ Command Invocation，彻底规避双重求值与不安全字符串拼接。
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">⚡</div>
    <div class="tcl-pillar-title">工业级 STA 静态时序分析门禁</div>
    <div class="tcl-pillar-desc">
      真实数字芯片时序报告解析实验，自动提取起点、终点与 Slack，精准计算 Worst Negative Slack (WNS) 与 Total Negative Slack (TNS)。
    </div>
  </div>
</div>

---

## 📚 课程体系索引 (40 周)

| 周次 | 课程专题 | 示例代码 |
| :---: | :--- | :---: |
{chr(10).join(zh_rows)}
"""
    (DOCS / "index.zh.md").write_text(zh_index, encoding="utf-8")


def generate_weeks() -> list[tuple[int, str, str]]:
    meta: list[tuple[int, str, str]] = []
    for wdir in week_dirs():
        week = int(wdir.name)
        en_raw = (wdir / "lesson_en.md").read_text(encoding="utf-8")
        zh_raw = (wdir / "lesson_zh.md").read_text(encoding="utf-8")
        en_h = first_heading(en_raw)
        zh_h = first_heading(zh_raw)
        en_short = short_title(en_h, week)
        zh_short = short_title(zh_h, week)

        out_dir = DOCS / "lessons" / f"week{week}"
        out_dir.mkdir(parents=True, exist_ok=True)

        en_body = rewrite_lesson_links(en_raw)
        zh_body = rewrite_lesson_links(zh_raw)

        (out_dir / "index.md").write_text(en_body, encoding="utf-8")
        (out_dir / "index.zh.md").write_text(zh_body, encoding="utf-8")
        (out_dir / "examples.md").write_text(examples_page(wdir, week, "en"), encoding="utf-8")
        (out_dir / "examples.zh.md").write_text(examples_page(wdir, week, "zh"), encoding="utf-8")

        meta.append((week, en_short, zh_short))
    return meta


def write_mkdocs_yml(meta: list[tuple[int, str, str]]) -> None:
    m10_nav, m20_nav, m30_nav, m40_nav = [], [], [], []
    nav_trans_weeks = []

    m_titles = [
        ("M10: Tcl Core Syntax (Weeks 01–10)", "M10: Tcl 核心语法 (第 01–10 周)"),
        ("M20: Fluency & OOP (Weeks 11–20)", "M20: 流畅编程与面向对象 (第 11–20 周)"),
        ("M30: Calibre Layout Core (Weeks 21–30)", "M30: Calibre 版图核心 (第 21–30 周)"),
        ("M40: Layout Catalog & Sign-Off (Weeks 31–40)", "M40: 版图全家桶与审计 (第 31–40 周)"),
    ]
    for en_m, zh_m in m_titles:
        nav_trans_weeks.append(f'            "{en_m}": "{zh_m}"')

    for w, en_title, zh_title in meta:
        item = (
            f'          - "Week {w:02d}: {en_title}":\n'
            f"              - Lesson: lessons/week{w}/index.md\n"
            f"              - Examples: lessons/week{w}/examples.md"
        )
        if w <= 10:
            m10_nav.append(item)
        elif w <= 20:
            m20_nav.append(item)
        elif w <= 30:
            m30_nav.append(item)
        else:
            m40_nav.append(item)
        nav_trans_weeks.append(f'            "Week {w:02d}: {en_title}": "第 {w:02d} 周: {zh_title}"')

    m10_yaml = "\n".join(m10_nav)
    m20_yaml = "\n".join(m20_nav)
    m30_yaml = "\n".join(m30_nav)
    m40_yaml = "\n".join(m40_nav)
    weeks_trans_yaml = "\n".join(nav_trans_weeks)

    yml = f"""# Generated by scripts/build_website.py — multi-language architecture
site_name: Tcl Language Lab
site_description: Bilingual Tcl / Calibre layout scripting lessons & Interactive WASM Workshop
site_url: https://sjtu-yongfu-research-grp.github.io/tcl-language/
repo_url: {GITHUB}
repo_name: tcl-language
edit_uri: ""

theme:
  name: material
  language: en
  palette:
    - scheme: default
      primary: teal
      accent: amber
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - scheme: slate
      primary: teal
      accent: amber
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode
  font:
    text: Inter
    code: Fira Code
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.highlight
    - content.code.copy
    - toc.follow

extra_css:
  - stylesheets/extra.css

extra:
  alternate:
    - name: English
      link: /
      lang: en
    - name: 简体中文
      link: /zh/
      lang: zh

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - tables
  - toc:
      permalink: true
  - pymdownx.tasklist:
      custom_checkbox: true

plugins:
  - search
  - i18n:
      docs_structure: suffix
      reconfigure_material: true
      reconfigure_search: true
      fallback_to_default: true
      languages:
        - locale: en
          default: true
          name: English
          build: true
        - locale: zh
          name: 简体中文
          build: true
          site_name: Tcl 工业级芯片自动化实验室
          site_description: 中英双语 Tcl / Calibre 版图自动化与时序分析全体系课程与交互工作坊
          nav_translations:
            Home: 首页
            Interactive Workshop (WASM): 交互工作坊 (WASM)
            Web Playground: 演练台 (Playground)
            Practice & Projects: 实战与项目
            18 Practical Exercises: 18 项实战练习
            6 Capstone Data Projects: 6 大综合项目
            Homework Assignments: 课后作业
            Chapter Quizzes: 随堂自测
            Lessons (40 Weeks): 课程体系 (40 周)
            EDA Tools & Guides: 工业工具与文档
            DRV-Lite Layout Simulator: DRV-Lite 版图仿真器
            STA Timing Analysis Lab: STA 时序分析门禁
            Tcl Mental Model Guide: Tcl 置换心智指南
            Calibre Command Reference: Calibre 常用命令速查
            Knowledge Graph Coverage: 知识图谱覆盖率
            Contributors: 致谢与贡献者
            Lesson: 课文
            Examples: 示例脚本
{weeks_trans_yaml}

validation:
  omitted_files: warn
  absolute_links: info
  unrecognized_links: warn

nav:
  - Home: index.md
  - Interactive Workshop (WASM): workshop.md
  - Web Playground: playground.md
  - Practice & Projects:
      - 18 Practical Exercises: exercises.md
      - 6 Capstone Data Projects: capstone.md
      - Homework Assignments: help/homework.md
      - Chapter Quizzes: help/quiz.md
  - Lessons (40 Weeks):
      - "M10: Tcl Core Syntax (Weeks 01–10)":
{m10_yaml}
      - "M20: Fluency & OOP (Weeks 11–20)":
{m20_yaml}
      - "M30: Calibre Layout Core (Weeks 21–30)":
{m30_yaml}
      - "M40: Layout Catalog & Sign-Off (Weeks 31–40)":
{m40_yaml}
  - EDA Tools & Guides:
      - DRV-Lite Layout Simulator: help/drvlite.md
      - STA Timing Analysis Lab: help/timing_lab.md
      - Tcl Mental Model Guide: help/tcl.md
      - Calibre Command Reference: help/calibre.md
      - Knowledge Graph Coverage: help/coverage.md
  - Contributors: contributors.md
"""
    (WEBSITE / "mkdocs.yml").write_text(yml, encoding="utf-8")


def clean_docs() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)


def main() -> None:
    clean_docs()
    meta = generate_weeks()
    if not meta:
        raise SystemExit("No lesson weeks found under lessons/")
    write_stylesheets()
    copy_workshop()
    copy_assets()
    write_workshop_pages()
    write_playground_pages()
    write_exercises_pages()
    write_capstone_pages()
    copy_help_docs()
    write_homework_pages()
    write_quiz_pages()
    write_contributors_pages()
    write_home_pages(meta)
    write_mkdocs_yml(meta)
    print(f"Generated multi-language website for {len(meta)} weeks -> {WEBSITE}")


if __name__ == "__main__":
    main()
