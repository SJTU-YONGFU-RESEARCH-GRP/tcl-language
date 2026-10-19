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
import sys
from pathlib import Path
from quiz_generator import write_quiz_challenge_pages, write_leaderboard_pages

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
        rf"^Lesson\s+{week}\s*[—–\-:]\s*",
        rf"^Week\s+{week}\s*[—–\-:]\s*",
        rf"^第\s*{week}\s*课\s*[—–\-:]\s*",
        rf"^第\s*{week}\s*周\s*[—–\-:]\s*",
        rf"^Pelajaran\s+{week}\s*[—–\-:]\s*",
        rf"^Leçon\s+{week}\s*[—–\-:]\s*",
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
            f"# 第 {week} 课 — 示例脚本",
            "",
            f"可在本地仓库运行：`make week{week}-NN`（见 [首页](../../index.md)）。",
            "",
        ]
    else:
        lines = [
            f"# Lesson {week} — Example Scripts",
            "",
            f"Run locally with `make week{week}-NN` (see [Home](../../index.md)).",
            "",
        ]
    if not tcl_files:
        lines.append("_No `.tcl` files in this lesson yet._")
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


def copy_quest() -> None:
    src = WEBSITE / "quest"
    if not src.exists():
        src_alt = ROOT.parent / "projects" / "su3037" / "site"
        if src_alt.exists():
            src = src_alt
    dst = DOCS / "quest-lab"
    if src.exists():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f"Copied standalone Tcl Quest (RPG) -> {dst}")


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
            (help_dir / dst_name.replace(".md", ".zh.md")).write_text(text, encoding="utf-8")
            (help_dir / dst_name.replace(".md", ".ms.md")).write_text(text, encoding="utf-8")
            (help_dir / dst_name.replace(".md", ".fr.md")).write_text(text, encoding="utf-8")


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

    ms_page = (
        "# Penyumbang & Penghargaan\n\n"
        f"Kolaborator kursus dan penyumbang projek pelajar cemerlang. Sumber: "
        f"[`CONTRIBUTORS.md`]({GITHUB}/blob/main/CONTRIBUTORS.md) "
        f"di GitHub.\n\n"
        f"{body}"
    )
    (DOCS / "contributors.ms.md").write_text(ms_page, encoding="utf-8")

    fr_page = (
        "# Contributeurs & Attribution\n\n"
        f"Collaborateurs du cours et contributeurs aux projets étudiants. Source : "
        f"[`CONTRIBUTORS.md`]({GITHUB}/blob/main/CONTRIBUTORS.md) "
        f"sur GitHub.\n\n"
        f"{body}"
    )
    (DOCS / "contributors.fr.md").write_text(fr_page, encoding="utf-8")


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
  <div style="background: var(--tcl-surface); padding: 12px 18px; border-bottom: 1px solid var(--tcl-border); display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
    <span><strong>Tcl WASM Interactive Lab</strong> · Powered by WebAssembly & FanqinZeng Workshop Engine</span>
    <a href="../wasm-lab/" target="_blank" style="color: var(--tcl-blue-600); font-weight: 600; text-decoration: none;">Launch Fullscreen ↗</a>
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
  <div style="background: var(--tcl-surface); padding: 12px 18px; border-bottom: 1px solid var(--tcl-border); display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
    <span><strong>Tcl WASM Interactive Lab</strong> · Powered by WebAssembly & FanqinZeng Workshop Engine</span>
    <a href="../wasm-lab/" target="_blank" style="color: var(--tcl-blue-600); font-weight: 600; text-decoration: none;">新标签页全屏打开 ↗</a>
  </div>
  <iframe src="../wasm-lab/" style="width: 100%; height: 880px; border: 0;" title="Tcl WASM Workshop"></iframe>
</div>
"""
    (DOCS / "workshop.zh.md").write_text(zh_content, encoding="utf-8")

    ms_content = (en_content
        .replace("# 🚀 Interactive Tcl Workshop (WASM)", "# 🚀 Bengkel Interaktif Tcl (WASM Lab)")
        .replace("A native Tcl 8.6.6 execution environment compiled to WebAssembly, featuring 18 guided exercises (54 hands-on tasks), 6 industrial data projects, and visual memory/variable inspector panels.",
                 "Persekitaran pelaksanaan Tcl 8.6.6 asli yang dikompilasi ke WebAssembly, menampilkan 18 latihan berpandu (54 tugasan amali), 6 projek data industri, dan panel visual pemeriksa pembolehubah/memori.")
        .replace("🚀 Launch Fullscreen Workshop ↗", "🚀 Buka Bengkel Skrin Penuh ↗")
        .replace("🎯 Explore 18 Exercises & Solutions →", "🎯 Terokai 18 Latihan & Penyelesaian →")
        .replace("🏆 Explore 6 Capstone Projects →", "🏆 Terokai 6 Projek Capstone →")
        .replace("## 🛠️ Key Architectural Highlights", "## 🛠️ Sorotan Seni Bina Utama")
        .replace("Client-Side WebAssembly Runtime", "Enjin WebAssembly Bahagian Pelanggan")
        .replace("Powered by WACL (WebAssembly Tcl 8.6.6). Code executes locally inside browser memory sandbox with zero server latency or network roundtrips.",
                 "Dikuasakan oleh WACL (WebAssembly Tcl 8.6.6). Kod dilaksanakan secara setempat dalam kotak pasir memori pelayar tanpa latensi pelayan.")
        .replace("18 Graded Labs & Auto-Testing", "18 Makmal Amali & Ujian Automatik")
        .replace("Visual Variable & Data Inspector", "Pemeriksa Visual Pembolehubah & Data")
        .replace("Industrial Datasets", "Set Data Industri Tulen")
        .replace("## 💻 Live In-Browser Laboratory", "## 💻 Makmal Langsung Dalam Pelayar")
        .replace("Interact directly with the embedded runner below, or launch fullscreen in a new tab:",
                 "Berinteraksi secara langsung dengan pelari terbenam di bawah, atau lancarkan skrin penuh dalam tab baharu:")
        .replace("Launch Fullscreen ↗", "Buka Skrin Penuh ↗")
    )
    (DOCS / "workshop.ms.md").write_text(ms_content, encoding="utf-8")

    fr_content = (en_content
        .replace("# 🚀 Interactive Tcl Workshop (WASM)", "# 🚀 Atelier Interactif Tcl (WASM Lab)")
        .replace("A native Tcl 8.6.6 execution environment compiled to WebAssembly, featuring 18 guided exercises (54 hands-on tasks), 6 industrial data projects, and visual memory/variable inspector panels.",
                 "Un environnement d'exécution natif Tcl 8.6.6 compilé en WebAssembly, comprenant 18 exercices guidés (54 tâches pratiques), 6 projets de données industrielles et des panneaux d'inspection visuelle de la mémoire et des variables.")
        .replace("🚀 Launch Fullscreen Workshop ↗", "🚀 Lancer l'Atelier Plein Écran ↗")
        .replace("🎯 Explore 18 Exercises & Solutions →", "🎯 Découvrir les 18 Exercices & Solutions →")
        .replace("🏆 Explore 6 Capstone Projects →", "🏆 Explorer les 6 Projets Capstone →")
        .replace("## 🛠️ Key Architectural Highlights", "## 🛠️ Points Forts de l'Architecture")
        .replace("Client-Side WebAssembly Runtime", "Moteur WebAssembly 100% Côté Client")
        .replace("Powered by WACL (WebAssembly Tcl 8.6.6). Code executes locally inside browser memory sandbox with zero server latency or network roundtrips.",
                 "Propulsé par WACL (WebAssembly Tcl 8.6.6). Le code s'exécute localement dans le bac à sable mémoire du navigateur sans latence de serveur.")
        .replace("18 Graded Labs & Auto-Testing", "18 Travaux Pratiques & Évaluation Automatique")
        .replace("Visual Variable & Data Inspector", "Inspecteur Visuel de Variables & Données")
        .replace("Industrial Datasets", "Jeux de Données Industriels Authentiques")
        .replace("## 💻 Live In-Browser Laboratory", "## 💻 Laboratoire Direct dans le Navigateur")
        .replace("Interact directly with the embedded runner below, or launch fullscreen in a new tab:",
                 "Interagissez directement avec l'exécuteur intégré ci-dessous, ou lancez-le en plein écran dans un nouvel onglet :")
        .replace("Launch Fullscreen ↗", "Lancer Plein Écran ↗")
    )
    (DOCS / "workshop.fr.md").write_text(fr_content, encoding="utf-8")


def write_quest_pages() -> None:
    en_content = f"""# 🎮 Tcl Quest — Chip Island Adventure

<div class="tcl-badge-cluster">
  <span class="tcl-badge purple">Execution-Driven RPG Sandbox</span>
  <span class="tcl-badge blue">WASM Tcl Engine</span>
  <span class="tcl-badge green">20 Graduated Levels</span>
  <span class="tcl-badge amber">Created by Su3037</span>
</div>

A groundbreaking gamified Tcl adventure created by **@Su3037** (rated **93/100 A+**). Code execution directly drives real-time character animations, visual level progression, interactive dialogues, and boss battles!

<div class="tcl-cta-group" style="margin: 20px 0 28px;">
  <a href="../quest-lab/index.html" target="_blank" class="tcl-btn tcl-btn-primary" style="font-size: 15px; padding: 12px 24px;">
    🚀 Launch Fullscreen Quest (Chip Island) ↗
  </a>
  <a href="../workshop/" class="tcl-btn tcl-btn-secondary" style="font-size: 15px; padding: 12px 24px;">
    ⚡ Switch to WASM Workshop →
  </a>
  <a href="../exercises/" class="tcl-btn tcl-btn-secondary" style="font-size: 15px; padding: 12px 24px;">
    🎯 18 Hands-on Exercises →
  </a>
</div>

---

## 🗺️ The Four Thematic Worlds

<div class="tcl-pillars">
  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🏡</div>
    <div class="tcl-pillar-title">World 01: Newbie Village (Levels 01–05)</div>
    <div class="tcl-pillar-desc">
      Awaken on Chip Island! Master <code>puts</code>, comments, variables, mathematical calculations, and string greetings.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🌲</div>
    <div class="tcl-pillar-title">World 02: Logic Forest (Levels 06–10)</div>
    <div class="tcl-pillar-desc">
      Navigate logic branches with <code>if/else</code>, <code>while</code>, <code>for</code> loops, lists, and procedures.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🔨</div>
    <div class="tcl-pillar-title">World 03: Tool Workshop (Levels 11–15)</div>
    <div class="tcl-pillar-desc">
      Harness industrial tool glue: dictionaries, file streams, regular expressions, namespaces, and runtime introspection.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🏙️</div>
    <div class="tcl-pillar-title">World 04: Chip City (Levels 16–20)</div>
    <div class="tcl-pillar-desc">
      Confront the final Boss! Build an automated digital IC static timing analysis (STA) report parser.
    </div>
  </div>
</div>

---

## 🕹️ Embedded Live Adventure

<div style="margin-top: 20px; border: 1px solid var(--tcl-border); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.06);">
  <div style="background: var(--tcl-surface); padding: 12px 18px; border-bottom: 1px solid var(--tcl-border); display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
    <span><strong>Tcl Quest Sandbox</strong> · Powered by Su3037 Execution-Driven RPG Engine</span>
    <a href="../quest-lab/index.html" target="_blank" style="color: var(--tcl-blue-600); font-weight: 600; text-decoration: none;">Launch Fullscreen ↗</a>
  </div>
  <iframe src="../quest-lab/index.html" style="width: 100%; height: 860px; border: 0;" title="Tcl Quest Adventure"></iframe>
</div>
"""
    (DOCS / "quest.md").write_text(en_content, encoding="utf-8")

    zh_content = f"""# 🎮 Tcl Quest — 芯片岛实时闯关冒险

<div class="tcl-badge-cluster">
  <span class="tcl-badge purple">真实代码驱动 live 剧情</span>
  <span class="tcl-badge blue">WASM Tcl 8.6 原生沙箱</span>
  <span class="tcl-badge green">20 个渐进冒险关卡</span>
  <span class="tcl-badge amber">开发者：Su3037 (93分 A+)</span>
</div>

整合来自 **@Su3037** 的 93 分 A+ 顶级教学创新：**真实 Tcl 代码执行驱动剧情动画**。用户在浏览器中编写并运行的每行代码、每个变量变化，都会实时触发角色走动、对话推进、Boss 挑战与关卡结算！

<div class="tcl-cta-group" style="margin: 20px 0 28px;">
  <a href="../quest-lab/index.html" target="_blank" class="tcl-btn tcl-btn-primary" style="font-size: 15px; padding: 12px 24px;">
    🚀 在新标签页全屏开启芯片岛冒险 ↗
  </a>
  <a href="../workshop/" class="tcl-btn tcl-btn-secondary" style="font-size: 15px; padding: 12px 24px;">
    ⚡ 切换至 WASM 自动化工作坊 →
  </a>
  <a href="../exercises/" class="tcl-btn tcl-btn-secondary" style="font-size: 15px; padding: 12px 24px;">
    🎯 浏览 18 项实战练习 →
  </a>
</div>

---

## 🗺️ 四大主题冒险世界

<div class="tcl-pillars">
  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🏡</div>
    <div class="tcl-pillar-title">第一世界 · 新手村 (第 01–05 关)</div>
    <div class="tcl-pillar-desc">
      在芯片岛醒来！从 <code>puts</code> 打印、注释、变量赋值、数学计算到格式化输出，迈出 Tcl 第一步。
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🌲</div>
    <div class="tcl-pillar-title">第二世界 · 逻辑森林 (第 06–10 关)</div>
    <div class="tcl-pillar-desc">
      穿越迷宫般的条件分支：<code>if/else</code>、<code>while</code>、<code>for</code> 循环、列表构建与自定义过程。
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🔨</div>
    <div class="tcl-pillar-title">第三世界 · 工具工坊 (第 11–15 关)</div>
    <div class="tcl-pillar-desc">
      掌握芯片胶水语言核心：字典映射、文件 I/O 流、正则表达式提取、命名空间与自省。
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🏙️</div>
    <div class="tcl-pillar-title">第四世界 · 芯片城 (第 16–20 关)</div>
    <div class="tcl-pillar-desc">
      迎战终极四大 Boss！亲手搭建数字芯片静态时序分析 (STA) 违规报表自动化分析器。
    </div>
  </div>
</div>

---

## 🕹️ 嵌入式实时冒险沙箱 (Embedded Sandbox)

可以在下方直接闯关，也可以点击上方按钮在新窗口中全屏畅玩：

<div style="margin-top: 20px; border: 1px solid var(--tcl-border); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.06);">
  <div style="background: var(--tcl-surface); padding: 12px 18px; border-bottom: 1px solid var(--tcl-border); display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
    <span><strong>芯片岛闯关沙箱</strong> · 真实代码驱动剧情 · 进度保存在此浏览器</span>
    <a href="../quest-lab/index.html" target="_blank" style="color: var(--tcl-blue-600); font-weight: 600; text-decoration: none;">新标签页全屏打开 ↗</a>
  </div>
  <iframe src="../quest-lab/index.html" style="width: 100%; height: 860px; border: 0;" title="Tcl Quest Adventure"></iframe>
</div>
"""
    (DOCS / "quest.zh.md").write_text(zh_content, encoding="utf-8")

    ms_content = (en_content
        .replace("# 🎮 Tcl Quest — Chip Island Adventure", "# 🎮 Tcl Quest — Pengembaraan Pulau Cip")
        .replace("A groundbreaking gamified Tcl adventure created by", "Pengembaraan Tcl gamifikasi cemerlang yang dicipta oleh")
        .replace("Code execution directly drives real-time character animations, visual level progression, interactive dialogues, and boss battles!",
                 "Pelaksanaan kod secara langsung menggerakkan animasi watak masa nyata, kemajuan tahap visual, dialog interaktif, dan pertempuran boss!")
        .replace("🚀 Launch Fullscreen Quest (Chip Island) ↗", "🚀 Buka Tcl Quest Skrin Penuh ↗")
        .replace("⚡ Switch to WASM Workshop →", "⚡ Beralih ke Bengkel WASM →")
        .replace("🎯 18 Hands-on Exercises →", "🎯 18 Latihan Amali →")
        .replace("## 🗺️ Four Themed Adventure Worlds", "## 🗺️ Empat Dunia Pengembaraan Bertema")
        .replace("World 1 · Starter Village (Levels 01–05)", "Dunia 1 · Kampung Permulaan (Tahap 01–05)")
        .replace("World 2 · Logic Forest (Levels 06–10)", "Dunia 2 · Hutan Logik (Tahap 06–10)")
        .replace("World 3 · Tools Workshop (Levels 11–15)", "Dunia 3 · Bengkel Alat (Tahap 11–15)")
        .replace("World 4 · Silicon City (Levels 16–20)", "Dunia 4 · Bandar Silikon (Tahap 16–20)")
        .replace("## 🕹️ Embedded Live Sandbox", "## 🕹️ Kotak Pasir Langsung Terbenam")
        .replace("Launch Fullscreen ↗", "Buka Skrin Penuh ↗")
    )
    (DOCS / "quest.ms.md").write_text(ms_content, encoding="utf-8")

    fr_content = (en_content
        .replace("# 🎮 Tcl Quest — Chip Island Adventure", "# 🎮 Tcl Quest — Aventure sur l'Île des Puces")
        .replace("A groundbreaking gamified Tcl adventure created by", "Une aventure Tcl gamifiée innovante créée par")
        .replace("Code execution directly drives real-time character animations, visual level progression, interactive dialogues, and boss battles!",
                 "L'exécution du code pilote directement les animations des personnages en temps réel, la progression visuelle des niveaux, les dialogues interactifs et les combats de boss !")
        .replace("🚀 Launch Fullscreen Quest (Chip Island) ↗", "🚀 Lancer Tcl Quest Plein Écran ↗")
        .replace("⚡ Switch to WASM Workshop →", "⚡ Basculer vers l'Atelier WASM →")
        .replace("🎯 18 Hands-on Exercises →", "🎯 18 Exercices Pratiques →")
        .replace("## 🗺️ Four Themed Adventure Worlds", "## 🗺️ Quatre Mondes d'Aventure Thématiques")
        .replace("World 1 · Starter Village (Levels 01–05)", "Monde 1 · Village de Départ (Niveaux 01–05)")
        .replace("World 2 · Logic Forest (Levels 06–10)", "Monde 2 · Forêt Logique (Niveaux 06–10)")
        .replace("World 3 · Tools Workshop (Levels 11–15)", "Monde 3 · Atelier d'Outils (Niveaux 11–15)")
        .replace("World 4 · Silicon City (Levels 16–20)", "Monde 4 · Cité Silicium (Niveaux 16–20)")
        .replace("## 🕹️ Embedded Live Sandbox", "## 🕹️ Bac à Sable Interactif Intégré")
        .replace("Launch Fullscreen ↗", "Lancer Plein Écran ↗")
    )
    (DOCS / "quest.fr.md").write_text(fr_content, encoding="utf-8")


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

    ms_content = (en_content
        .replace("# 🎯 18 Practical Exercises (54 Coding Tasks)", "# 🎯 18 Latihan Amali (54 Tugasan Pengekodan)")
        .replace("Curated from FanqinZeng's top-ranked educational project (Audit Score 98/100), this suite provides **18 modular practice units** (comprising 54 graduated tasks). Each module features authentic engineering data, starter code templates, test criteria, and verified reference solutions.",
                 "Disusun daripada projek pendidikan terbaik FanqinZeng (Skor Audit 98/100), suite ini menyediakan **18 unit latihan modular** (merangkumi 54 tugasan bertahap). Setiap modul menampilkan data kejuruteraan tulen, templat kod permulaan, kriteria ujian, dan penyelesaian rujukan yang disahkan.")
        .replace("Execute them directly in our [🚀 Interactive WASM Lab](workshop.md) or clone locally to run under standard `tclsh`.",
                 "Laksanakannya secara langsung dalam [🚀 Bengkel Interaktif WASM](workshop.md) kami atau klon secara tempatan untuk dijalankan di bawah `tclsh` standard.")
        .replace("## 📋 Exercise Directory", "## 📋 Direktori Latihan")
        .replace("Key Skills & Tasks", "Kemahiran Utama & Tugasan")
        .replace("Starter", "Permulaan")
        .replace("Solution", "Penyelesaian")
    )
    (DOCS / "exercises.ms.md").write_text(ms_content, encoding="utf-8")

    fr_content = (en_content
        .replace("# 🎯 18 Practical Exercises (54 Coding Tasks)", "# 🎯 18 Exercices Pratiques (54 Tâches de Code)")
        .replace("Curated from FanqinZeng's top-ranked educational project (Audit Score 98/100), this suite provides **18 modular practice units** (comprising 54 graduated tasks). Each module features authentic engineering data, starter code templates, test criteria, and verified reference solutions.",
                 "Issu du projet éducatif d'excellence de FanqinZeng (Score d'audit 98/100), cet ensemble propose **18 unités de pratique modulaire** (54 tâches progressives). Chaque module intègre des données d'ingénierie authentiques, des modèles de code de départ, des critères de test et des solutions de référence vérifiées.")
        .replace("Execute them directly in our [🚀 Interactive WASM Lab](workshop.md) or clone locally to run under standard `tclsh`.",
                 "Exécutez-les directement dans notre [🚀 Atelier Interactif WASM](workshop.md) ou clonez localement sous un interpréteur `tclsh` standard.")
        .replace("## 📋 Exercise Directory", "## 📋 Répertoire des Exercices")
        .replace("Key Skills & Tasks", "Compétences Clés & Tâches")
        .replace("Starter", "Départ")
        .replace("Solution", "Solution")
    )
    (DOCS / "exercises.fr.md").write_text(fr_content, encoding="utf-8")


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

    ms_content = (en_content
        .replace("# 🏆 6 Capstone Data Engineering Projects", "# 🏆 6 Projek Capstone Kejuruteraan Data")
        .replace("In addition to foundational exercises, this curriculum incorporates 6 major capstone data engineering projects (Projects A–F). Each project models real-world chip development, server administration, or enterprise data workflows, complete with automated test suites (`case-1.tcl` through `case-4.tcl`), starter templates, and reference implementations.",
                 "Selain latihan asas, kurikulum ini menggabungkan 6 projek kejuruteraan data capstone utama (Projek A–F). Setiap projek memodelkan pembangunan cip dunia sebenar, pentadbiran pelayan, atau aliran kerja data perusahaan, lengkap dengan suite ujian automatik (`case-1.tcl` hingga `case-4.tcl`), templat permulaan, dan pelaksanaan rujukan.")
        .replace("## 📁 Project Matrix", "## 📁 Matriks Projek")
        .replace("View Project Spec →", "Lihat Spesifikasi Projek →")
        .replace("Solution Source", "Kod Sumber Penyelesaian")
    )
    (DOCS / "capstone.ms.md").write_text(ms_content, encoding="utf-8")

    fr_content = (en_content
        .replace("# 🏆 6 Capstone Data Engineering Projects", "# 🏆 6 Projets Capstone d'Ingénierie des Données")
        .replace("In addition to foundational exercises, this curriculum incorporates 6 major capstone data engineering projects (Projects A–F). Each project models real-world chip development, server administration, or enterprise data workflows, complete with automated test suites (`case-1.tcl` through `case-4.tcl`), starter templates, and reference implementations.",
                 "En plus des exercices de base, ce programme intègre 6 grands projets d'ingénierie des données (Projets A–F). Chaque projet modélise le développement de puces réelles, l'administration de serveurs ou des flux de données d'entreprise, avec suites de tests automatisés (`case-1.tcl` à `case-4.tcl`), modèles de démarrage et implémentations de référence.")
        .replace("## 📁 Project Matrix", "## 📁 Matrice des Projets")
        .replace("View Project Spec →", "Voir la Spécification du Projet →")
        .replace("Solution Source", "Code Source de la Solution")
    )
    (DOCS / "capstone.fr.md").write_text(fr_content, encoding="utf-8")


def write_homework_pages() -> None:
    (DOCS / "help").mkdir(parents=True, exist_ok=True)
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
    (DOCS / "help" / "homework.ms.md").write_text(body, encoding="utf-8")
    (DOCS / "help" / "homework.fr.md").write_text(body, encoding="utf-8")


def write_quiz_pages() -> None:
    (DOCS / "help").mkdir(parents=True, exist_ok=True)
    en_page = f"""# Chapter Quizzes & Knowledge Checks

<div class="tcl-badge-cluster">
  <span class="tcl-badge">Chapter Quizzes</span>
  <span class="tcl-badge amber">Knowledge Checks</span>
  <span class="tcl-badge blue">Tcl Knowledge Assessment</span>
  <span class="tcl-badge purple">Verifiable Certificates</span>
  <span class="tcl-badge green">Public Leaderboard</span>
</div>

Curated from thy031's student project, this module provides rapid knowledge checks across core Tcl syntax, lists, dictionaries, and procedure scripting.

<div style="margin: 20px 0; display:flex; gap:12px; flex-wrap:wrap;">
  <a href="../../quiz/" class="tcl-btn tcl-btn-primary">🎯 Launch Quiz Challenge →</a>
  <a href="../../leaderboard/" class="tcl-btn tcl-btn-secondary">🏆 View Public Leaderboard & Certificates →</a>
</div>

- **Mental Model Checks**: Substitution timing comparison between `set x $a` and `set x {{a}}`.
- **Evaluation Safety**: Anti-injection checks on braced `expr {{$a + $b}}` vs unquoted variants.
- **Data Structures**: List boundaries, dictionary value extraction, and nested loops.
- **Scripting Automation**: Procedures, return values, control flow, and error handling.
"""
    (DOCS / "help" / "quiz.md").write_text(en_page, encoding="utf-8")

    zh_page = f"""# 随堂自测题库与交互答题 (Interactive Quizzes)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">章节自测题库</span>
  <span class="tcl-badge amber">快速检验</span>
  <span class="tcl-badge blue">Tcl 核心语法检验</span>
  <span class="tcl-badge purple">防伪认证证书</span>
  <span class="tcl-badge green">荣誉排行榜</span>
</div>

本测验模块源自 thy031 同学的学习项目，提供涵盖 Tcl 基础语法、列表字典、控制流与过程函数等核心主题的交互式知识自测与结课证书。

<div style="margin: 20px 0; display:flex; gap:12px; flex-wrap:wrap;">
  <a href="../../quiz/" class="tcl-btn tcl-btn-primary">🎯 开启随堂评测挑战 (Quiz Challenge) →</a>
  <a href="../../leaderboard/" class="tcl-btn tcl-btn-secondary">🏆 查看全网荣誉排行榜与证书 →</a>
</div>

- **语法心智自测**：辨析 `set x $a` 与 `set x {{a}}` 的置换时机差异。
- **求值规则测试**：严格花括号 `expr {{$a + $b}}` 与无保护 `expr $a + $b` 的安全评测。
- **数据结构实战**：列表索引边界、字典键值提取与嵌套遍历。
- **脚本自动化**：过程封装、返回值传递与条件循环控制。
"""
    (DOCS / "help" / "quiz.zh.md").write_text(zh_page, encoding="utf-8")

    ms_page = (en_page
        .replace("# Chapter Quizzes & Knowledge Checks", "# Kuiz Bab & Semakan Pengetahuan (Interactive Quizzes)")
        .replace("Curated from thy031's student project, this module provides rapid knowledge checks across core Tcl syntax, lists, dictionaries, and procedure scripting.",
                 "Disusun daripada projek pelajar thy031, modul ini menyediakan semakan pantas pengetahuan merangkumi sintaks teras Tcl, senarai, kamus, dan skrip prosedur dengan sijil digital.")
        .replace("🎯 Launch Quiz Challenge →", "🎯 Lancarkan Cabaran Kuiz →")
        .replace("🏆 View Public Leaderboard & Certificates →", "🏆 Lihat Papan Pendahulu & Sijil →")
    )
    (DOCS / "help" / "quiz.ms.md").write_text(ms_page, encoding="utf-8")

    fr_page = (en_page
        .replace("# Chapter Quizzes & Knowledge Checks", "# Quiz de Chapitre & Vérification des Connaissances (Interactive Quizzes)")
        .replace("Curated from thy031's student project, this module provides rapid knowledge checks across core Tcl syntax, lists, dictionaries, and procedure scripting.",
                 "Issu du projet étudiant de thy031, ce module propose des contrôles de connaissances rapides sur la syntaxe Tcl, les listes, les dictionnaires et les procédures avec certificats numériques vérifiables.")
        .replace("🎯 Launch Quiz Challenge →", "🎯 Lancer le Défi Quiz →")
        .replace("🏆 View Public Leaderboard & Certificates →", "🏆 Voir le Classement & Certificats →")
    )
    (DOCS / "help" / "quiz.fr.md").write_text(fr_page, encoding="utf-8")


def write_playground_pages() -> None:
    en_header = """# ⚡ Interactive Tcl Web Playground

<div class="tcl-badge-cluster">
  <span class="tcl-badge blue">Zero-Install Runtime</span>
  <span class="tcl-badge green">Pure JavaScript Engine</span>
  <span class="tcl-badge purple">Live Syntax Checks</span>
  <span class="tcl-badge amber">Preset Code Examples</span>
</div>

Test, experiment, and run Tcl scripts directly in your browser without local installation. Load presets below or write custom scripts.

<div style="background: var(--tcl-surface); border: 1px solid var(--tcl-border); border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
  <div style="display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; align-items: center;">
    <span style="font-weight: 700; font-size: 13px; color: var(--tcl-heading);">Load Presets:</span>
    <button onclick="loadSnippet('hello')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">01. Hello puts</button>
    <button onclick="loadSnippet('subst')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">02. Welch Mental Model</button>
    <button onclick="loadSnippet('expr')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">03. Braced expr</button>
    <button onclick="loadSnippet('list_dict')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">04. List & Dict</button>
    <button onclick="loadSnippet('timing')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">05. STA Slack Parser</button>
    <button onclick="loadSnippet('drvlite')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">06. DRV-Lite Layout</button>
  </div>

  <textarea id="tcl-code-input" style="width: 100%; height: 210px; font-family: 'JetBrains Mono', monospace; background: #0f172a; color: #f8fafc; border: 1px solid var(--tcl-border); border-radius: 8px; padding: 14px; box-sizing: border-box; font-size: 13.5px; line-height: 1.6; resize: vertical; outline: none;"></textarea>

  <div style="margin-top: 12px; display: flex; gap: 10px; align-items: center; justify-content: space-between; flex-wrap: wrap;">
    <div style="display: flex; gap: 10px; align-items: center;">
      <button onclick="runTclCode()" class="tcl-btn tcl-btn-primary" style="padding: 8px 20px; font-size: 13px;">▶ Run Script (Ctrl+Enter)</button>
      <button onclick="clearOutput()" class="tcl-btn tcl-btn-secondary" style="padding: 8px 14px; font-size: 13px;">Clear Console</button>
    </div>
    <span id="tcl-status" style="font-size: 12px; color: #10b981; font-weight: 600;">Ready</span>
  </div>

  <div style="margin-top: 16px;">
    <div style="font-size: 12px; color: var(--md-default-fg-color--lighter); margin-bottom: 6px; font-weight: 700;">Standard Console Output:</div>
    <pre id="tcl-output" style="background: #020617; color: #34d399; border: 1px solid #1e293b; border-radius: 8px; padding: 14px; min-height: 90px; max-height: 250px; overflow-y: auto; font-family: 'JetBrains Mono', monospace; font-size: 13px; margin: 0; white-space: pre-wrap; line-height: 1.5;"></pre>
  </div>
</div>
"""
    script_part = """<script>
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
"""
    zh_header = """# ⚡ Tcl 在线快速演练台 (Interactive Playground)

<div class="tcl-badge-cluster">
  <span class="tcl-badge blue">免安装在线运行</span>
  <span class="tcl-badge green">纯前端即时执行</span>
  <span class="tcl-badge purple">实时语法校验</span>
  <span class="tcl-badge amber">内置经典示例</span>
</div>

无需本地安装任何环境，直接在浏览器中编写、测试并运行 Tcl 脚本。可在上方点击加载预设示例，或自由编辑代码体验。

<div style="background: var(--tcl-surface); border: 1px solid var(--tcl-border); border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
  <div style="display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; align-items: center;">
    <span style="font-weight: 700; font-size: 13px; color: var(--tcl-heading);">加载示例预设:</span>
    <button onclick="loadSnippet('hello')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">01. Hello puts</button>
    <button onclick="loadSnippet('subst')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">02. 置换心智模型</button>
    <button onclick="loadSnippet('expr')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">03. 安全花括号 expr</button>
    <button onclick="loadSnippet('list_dict')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">04. 列表与字典</button>
    <button onclick="loadSnippet('timing')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">05. STA 时序解析</button>
    <button onclick="loadSnippet('drvlite')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">06. DRV-Lite 版图</button>
  </div>

  <textarea id="tcl-code-input" style="width: 100%; height: 210px; font-family: 'JetBrains Mono', monospace; background: #0f172a; color: #f8fafc; border: 1px solid var(--tcl-border); border-radius: 8px; padding: 14px; box-sizing: border-box; font-size: 13.5px; line-height: 1.6; resize: vertical; outline: none;"></textarea>

  <div style="margin-top: 12px; display: flex; gap: 10px; align-items: center; justify-content: space-between; flex-wrap: wrap;">
    <div style="display: flex; gap: 10px; align-items: center;">
      <button onclick="runTclCode()" class="tcl-btn tcl-btn-primary" style="padding: 8px 20px; font-size: 13px;">▶ 运行脚本 (Ctrl+Enter)</button>
      <button onclick="clearOutput()" class="tcl-btn tcl-btn-secondary" style="padding: 8px 14px; font-size: 13px;">清空控制台</button>
    </div>
    <span id="tcl-status" style="font-size: 12px; color: #10b981; font-weight: 600;">就绪</span>
  </div>

  <div style="margin-top: 16px;">
    <div style="font-size: 12px; color: var(--md-default-fg-color--lighter); margin-bottom: 6px; font-weight: 700;">标准控制台输出:</div>
    <pre id="tcl-output" style="background: #020617; color: #34d399; border: 1px solid #1e293b; border-radius: 8px; padding: 14px; min-height: 90px; max-height: 250px; overflow-y: auto; font-family: 'JetBrains Mono', monospace; font-size: 13px; margin: 0; white-space: pre-wrap; line-height: 1.5;"></pre>
  </div>
</div>
"""
    en_footer = """
---

## Standalone WebAssembly Tcl IDE

Looking for full in-browser test grading, step-by-step interactive debugging, and memory table inspector? Launch the [🚀 Interactive Workshop (WASM)](workshop.md).
"""
    zh_footer = """
---

## 独立 WebAssembly 完整 Tcl IDE

如需包含 18 项实战评测、变量内存树监视器与单步断点调试的完整开发环境，请启动 [🚀 交互工作坊 (WASM)](workshop.md)。
"""
    ms_header = """# ⚡ Taman Permainan Pantas Tcl Atas Talian (Interactive Playground)

<div class="tcl-badge-cluster">
  <span class="tcl-badge blue">Jalankan Tanpa Pemasangan</span>
  <span class="tcl-badge green">Pelaksanaan Frontend Segera</span>
  <span class="tcl-badge purple">Pengesahan Sintaks Masa Nyata</span>
  <span class="tcl-badge amber">Pratetap Kod Contoh</span>
</div>

Uji, bereksperimen, dan jalankan skrip Tcl terus dalam pelayar anda tanpa sebarang pemasangan tempatan. Muat pratetap di bawah atau tulis skrip tersuai anda sendiri.

<div style="background: var(--tcl-surface); border: 1px solid var(--tcl-border); border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
  <div style="display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; align-items: center;">
    <span style="font-weight: 700; font-size: 13px; color: var(--tcl-heading);">Muat Pratetap:</span>
    <button onclick="loadSnippet('hello')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">01. Hello puts</button>
    <button onclick="loadSnippet('subst')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">02. Model Mental Welch</button>
    <button onclick="loadSnippet('expr')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">03. expr Kurungan Selamat</button>
    <button onclick="loadSnippet('list_dict')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">04. Senarai & Kamus</button>
    <button onclick="loadSnippet('timing')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">05. Pengurai Slack STA</button>
    <button onclick="loadSnippet('drvlite')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">06. Susun Atur DRV-Lite</button>
  </div>

  <textarea id="tcl-code-input" style="width: 100%; height: 210px; font-family: 'JetBrains Mono', monospace; background: #0f172a; color: #f8fafc; border: 1px solid var(--tcl-border); border-radius: 8px; padding: 14px; box-sizing: border-box; font-size: 13.5px; line-height: 1.6; resize: vertical; outline: none;"></textarea>

  <div style="margin-top: 12px; display: flex; gap: 10px; align-items: center; justify-content: space-between; flex-wrap: wrap;">
    <div style="display: flex; gap: 10px; align-items: center;">
      <button onclick="runTclCode()" class="tcl-btn tcl-btn-primary" style="padding: 8px 20px; font-size: 13px;">▶ Jalankan Skrip (Ctrl+Enter)</button>
      <button onclick="clearOutput()" class="tcl-btn tcl-btn-secondary" style="padding: 8px 14px; font-size: 13px;">Kosongkan Konsol</button>
    </div>
    <span id="tcl-status" style="font-size: 12px; color: #10b981; font-weight: 600;">Sedia</span>
  </div>

  <div style="margin-top: 16px;">
    <div style="font-size: 12px; color: var(--md-default-fg-color--lighter); margin-bottom: 6px; font-weight: 700;">Output Konsol Piawai:</div>
    <pre id="tcl-output" style="background: #020617; color: #34d399; border: 1px solid #1e293b; border-radius: 8px; padding: 14px; min-height: 90px; max-height: 250px; overflow-y: auto; font-family: 'JetBrains Mono', monospace; font-size: 13px; margin: 0; white-space: pre-wrap; line-height: 1.5;"></pre>
  </div>
</div>
"""
    ms_footer = """
---

## IDE Tcl WebAssembly Lengkap & Mandiri

Mencari persekitaran pembangunan lengkap dengan penggredan ujian 18 modul, pemantau pembolehubah memori, dan penyahpepijatan langkah demi langkah? Lancarkan [🚀 Bengkel Interaktif (WASM)](workshop.md).
"""
    fr_header = """# ⚡ Bac à Sable Tcl Interactif Rapide (Interactive Playground)

<div class="tcl-badge-cluster">
  <span class="tcl-badge blue">Exécution Sans Installation</span>
  <span class="tcl-badge green">Purement Côté Client</span>
  <span class="tcl-badge purple">Validation en Temps Réel</span>
  <span class="tcl-badge amber">Exemples Intégrés</span>
</div>

Testez, expérimentez et exécutez des scripts Tcl directement dans votre navigateur sans aucune installation locale. Chargez des préréglages ci-dessous ou écrivez votre propre code.

<div style="background: var(--tcl-surface); border: 1px solid var(--tcl-border); border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
  <div style="display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; align-items: center;">
    <span style="font-weight: 700; font-size: 13px; color: var(--tcl-heading);">Charger un Exemple :</span>
    <button onclick="loadSnippet('hello')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">01. Hello puts</button>
    <button onclick="loadSnippet('subst')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">02. Modèle Mental de Welch</button>
    <button onclick="loadSnippet('expr')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">03. expr avec Accolades Sûres</button>
    <button onclick="loadSnippet('list_dict')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">04. Listes & Dictionnaires</button>
    <button onclick="loadSnippet('timing')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">05. Analyseur de Slack STA</button>
    <button onclick="loadSnippet('drvlite')" class="tcl-btn tcl-btn-secondary" style="padding: 5px 12px; font-size: 12px;">06. Layout DRV-Lite</button>
  </div>

  <textarea id="tcl-code-input" style="width: 100%; height: 210px; font-family: 'JetBrains Mono', monospace; background: #0f172a; color: #f8fafc; border: 1px solid var(--tcl-border); border-radius: 8px; padding: 14px; box-sizing: border-box; font-size: 13.5px; line-height: 1.6; resize: vertical; outline: none;"></textarea>

  <div style="margin-top: 12px; display: flex; gap: 10px; align-items: center; justify-content: space-between; flex-wrap: wrap;">
    <div style="display: flex; gap: 10px; align-items: center;">
      <button onclick="runTclCode()" class="tcl-btn tcl-btn-primary" style="padding: 8px 20px; font-size: 13px;">▶ Exécuter le Script (Ctrl+Enter)</button>
      <button onclick="clearOutput()" class="tcl-btn tcl-btn-secondary" style="padding: 8px 14px; font-size: 13px;">Effacer la Console</button>
    </div>
    <span id="tcl-status" style="font-size: 12px; color: #10b981; font-weight: 600;">Prêt</span>
  </div>

  <div style="margin-top: 16px;">
    <div style="font-size: 12px; color: var(--md-default-fg-color--lighter); margin-bottom: 6px; font-weight: 700;">Sortie Standard Console :</div>
    <pre id="tcl-output" style="background: #020617; color: #34d399; border: 1px solid #1e293b; border-radius: 8px; padding: 14px; min-height: 90px; max-height: 250px; overflow-y: auto; font-family: 'JetBrains Mono', monospace; font-size: 13px; margin: 0; white-space: pre-wrap; line-height: 1.5;"></pre>
  </div>
</div>
"""
    fr_footer = """
---

## IDE WebAssembly Tcl Autonome & Complet

Vous cherchez un environnement de développement complet avec notation de 18 exercices pratiques, inspecteur de variables mémoire et débogage pas à pas ? Lancez l'[🚀 Atelier Interactif (WASM)](workshop.md).
"""
    (DOCS / "playground.md").write_text(en_header + "\n" + script_part + "\n" + en_footer, encoding="utf-8")
    (DOCS / "playground.zh.md").write_text(zh_header + "\n" + script_part + "\n" + zh_footer, encoding="utf-8")
    (DOCS / "playground.ms.md").write_text(ms_header + "\n" + script_part + "\n" + ms_footer, encoding="utf-8")
    (DOCS / "playground.fr.md").write_text(fr_header + "\n" + script_part + "\n" + fr_footer, encoding="utf-8")


def write_layout_viewer_pages() -> None:
    (DOCS / "help").mkdir(parents=True, exist_ok=True)
    en_content = """# 📐 Interactive VLSI Layout Visualizer (DRV-Lite Simulator)

<div class="tcl-badge-cluster">
  <span class="tcl-badge blue">DRV-Lite Pure-Tcl Engine</span>
  <span class="tcl-badge green">Zero Commercial License</span>
  <span class="tcl-badge cyan">Interactive 2D Canvas</span>
  <span class="tcl-badge purple">GDS II / OASIS Ready</span>
</div>

A real-time in-browser semiconductor layout visualizer inspired by Capeur's pure-Tcl **DRV-Lite** engine. Inspect multi-layer IC cell geometries, toggle metal routing tracks, observe bounding box snaps, and execute Tcl layout commands directly in the browser!

---

<div class="layout-viewer-container" style="background: var(--tcl-surface); border: 1px solid var(--tcl-border); border-radius: 12px; padding: 20px; margin: 24px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
  
  <!-- Toolbar -->
  <div style="display: flex; gap: 12px; flex-wrap: wrap; align-items: center; justify-content: space-between; margin-bottom: 14px;">
    <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
      <span style="font-weight: 700; font-size: 13px; color: var(--md-default-fg-color);">Cell Preset:</span>
      <select id="cellPresetSelect" onchange="loadLayoutPreset(this.value)" style="background: var(--md-default-bg-color); color: var(--md-default-fg-color); border: 1px solid var(--tcl-border); border-radius: 6px; padding: 6px 12px; font-size: 13px; cursor: pointer; outline: none;">
        <option value="inv">CMOS Inverter (INV_X1)</option>
        <option value="nand2">2-Input NAND (NAND2_X1)</option>
        <option value="routing">M1/M2 Cross-Routing with VIA1</option>
        <option value="pad">I/O Bond Pad & Guard Ring</option>
      </select>
    </div>

    <div style="display: flex; gap: 6px; align-items: center;">
      <button onclick="zoomCanvas(1.2)" class="tcl-btn tcl-btn-secondary" style="padding: 4px 10px; font-size: 13px;">🔍+ Zoom In</button>
      <button onclick="zoomCanvas(0.8)" class="tcl-btn tcl-btn-secondary" style="padding: 4px 10px; font-size: 13px;">🔍- Zoom Out</button>
      <button onclick="resetCanvas()" class="tcl-btn tcl-btn-secondary" style="padding: 4px 10px; font-size: 13px;">⟲ Reset</button>
      <button id="gridToggleBtn" onclick="toggleGrid()" class="tcl-btn tcl-btn-secondary" style="padding: 4px 10px; font-size: 13px;">Grid: ON</button>
      <button id="bboxToggleBtn" onclick="toggleBBox()" class="tcl-btn tcl-btn-secondary" style="padding: 4px 10px; font-size: 13px;">BBox: ON</button>
    </div>
  </div>

  <!-- Layer Filter Palette -->
  <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 12px; padding: 8px 12px; background: var(--md-default-bg-color); border: 1px solid var(--tcl-border); border-radius: 6px; font-size: 12px;">
    <span style="font-weight: 700; align-self: center;">Layers:</span>
    <label style="cursor: pointer; display: flex; align-items: center; gap: 4px;"><input type="checkbox" checked onchange="toggleLayer(1, this.checked)"> <span style="display:inline-block; width:10px; height:10px; background:#f59e0b; border-radius:2px;"></span> NWEL (1)</label>
    <label style="cursor: pointer; display: flex; align-items: center; gap: 4px;"><input type="checkbox" checked onchange="toggleLayer(2, this.checked)"> <span style="display:inline-block; width:10px; height:10px; background:#10b981; border-radius:2px;"></span> DIFF (2)</label>
    <label style="cursor: pointer; display: flex; align-items: center; gap: 4px;"><input type="checkbox" checked onchange="toggleLayer(3, this.checked)"> <span style="display:inline-block; width:10px; height:10px; background:#ef4444; border-radius:2px;"></span> POLY (3)</label>
    <label style="cursor: pointer; display: flex; align-items: center; gap: 4px;"><input type="checkbox" checked onchange="toggleLayer(4, this.checked)"> <span style="display:inline-block; width:10px; height:10px; background:#94a3b8; border-radius:2px;"></span> CONT (4)</label>
    <label style="cursor: pointer; display: flex; align-items: center; gap: 4px;"><input type="checkbox" checked onchange="toggleLayer(5, this.checked)"> <span style="display:inline-block; width:10px; height:10px; background:#3b82f6; border-radius:2px;"></span> M1 (5)</label>
    <label style="cursor: pointer; display: flex; align-items: center; gap: 4px;"><input type="checkbox" checked onchange="toggleLayer(6, this.checked)"> <span style="display:inline-block; width:10px; height:10px; background:#ec4899; border-radius:2px;"></span> VIA1 (6)</label>
    <label style="cursor: pointer; display: flex; align-items: center; gap: 4px;"><input type="checkbox" checked onchange="toggleLayer(7, this.checked)"> <span style="display:inline-block; width:10px; height:10px; background:#06b6d4; border-radius:2px;"></span> M2 (7)</label>
  </div>

  <!-- HTML5 Canvas Visualizer -->
  <div style="position: relative; width: 100%; border-radius: 8px; overflow: hidden; border: 1px solid var(--tcl-border);">
    <canvas id="chipCanvas" width="840" height="420" style="width: 100%; height: 420px; background: #070d18; display: block; cursor: crosshair;"></canvas>
    
    <!-- Floating Coordinate Overlay -->
    <div id="coordOverlay" style="position: absolute; bottom: 8px; left: 8px; background: rgba(15, 23, 42, 0.85); color: #94a3b8; font-family: monospace; font-size: 11px; padding: 4px 10px; border-radius: 4px; pointer-events: none; border: 1px solid rgba(255,255,255,0.1);">
      Cursor: X: 0.00 um, Y: 0.00 um | BBox: [0.0 0.0 1200.0 650.0] | Scale: 1.0x
    </div>
  </div>

  <!-- Interactive Tcl Command Line -->
  <div style="margin-top: 16px; display: flex; gap: 8px; flex-wrap: wrap;">
    <input type="text" id="tclLayoutCmdInput" value="$L create box TOP 5 150 200 550 450" style="flex: 1; min-width: 280px; background: var(--md-code-bg-color); color: #f8fafc; border: 1px solid var(--tcl-border); border-radius: 6px; padding: 10px 14px; font-family: monospace; font-size: 13px; outline: none;">
    <button onclick="executeLayoutCmd()" class="tcl-btn tcl-btn-primary" style="padding: 10px 18px; font-size: 13px;">⚡ Execute Tcl Command</button>
  </div>
  <div id="layoutCmdLog" style="margin-top: 8px; font-family: monospace; font-size: 12px; color: #10b981;">Ready. Select a preset cell or enter a layout command.</div>
</div>

<script>
const canvas = document.getElementById('chipCanvas');
const ctx = canvas.getContext('2d');
let zoom = 1.0;
let panX = 120, panY = 70;
let showGrid = true;
let showBBox = true;

const layerColors = {
  1: 'rgba(245, 158, 11, 0.45)',  // NWEL
  2: 'rgba(16, 185, 129, 0.55)',  // DIFF
  3: 'rgba(239, 68, 68, 0.70)',   // POLY
  4: 'rgba(148, 163, 184, 0.85)', // CONT
  5: 'rgba(59, 130, 246, 0.65)',  // M1
  6: 'rgba(236, 72, 153, 0.85)',  // VIA1
  7: 'rgba(6, 182, 212, 0.65)'    // M2
};

const layerVisible = { 1: true, 2: true, 3: true, 4: true, 5: true, 6: true, 7: true };

let currentGeoms = [];

const cellPresets = {
  inv: [
    { layer: 1, x: 50, y: 150, w: 500, h: 250, label: 'NWEL' },
    { layer: 2, x: 80, y: 50, w: 440, h: 80, label: 'DIFF (NMOS)' },
    { layer: 2, x: 80, y: 200, w: 440, h: 160, label: 'DIFF (PMOS)' },
    { layer: 3, x: 250, y: 30, w: 60, h: 360, label: 'POLY (GATE)' },
    { layer: 4, x: 120, y: 70, w: 30, h: 30 },
    { layer: 4, x: 420, y: 70, w: 30, h: 30 },
    { layer: 4, x: 120, y: 260, w: 30, h: 30 },
    { layer: 4, x: 420, y: 260, w: 30, h: 30 },
    { layer: 5, x: 30, y: 370, w: 540, h: 50, label: 'M1 (VDD RAIL)' },
    { layer: 5, x: 30, y: 10, w: 540, h: 50, label: 'M1 (GND RAIL)' },
    { layer: 5, x: 390, y: 60, w: 90, h: 260, label: 'M1 (OUT)' }
  ],
  nand2: [
    { layer: 1, x: 50, y: 160, w: 650, h: 240, label: 'NWEL' },
    { layer: 2, x: 80, y: 50, w: 580, h: 90, label: 'DIFF (NMOS)' },
    { layer: 2, x: 80, y: 210, w: 580, h: 160, label: 'DIFF (PMOS)' },
    { layer: 3, x: 220, y: 30, w: 50, h: 360, label: 'POLY (IN_A)' },
    { layer: 3, x: 420, y: 30, w: 50, h: 360, label: 'POLY (IN_B)' },
    { layer: 5, x: 30, y: 380, w: 700, h: 50, label: 'M1 (VDD)' },
    { layer: 5, x: 30, y: 10, w: 700, h: 50, label: 'M1 (GND)' },
    { layer: 5, x: 520, y: 60, w: 80, h: 280, label: 'M1 (OUT)' }
  ],
  routing: [
    { layer: 5, x: 50, y: 100, w: 600, h: 40, label: 'M1_TRACK_0' },
    { layer: 5, x: 50, y: 220, w: 600, h: 40, label: 'M1_TRACK_1' },
    { layer: 5, x: 50, y: 340, w: 600, h: 40, label: 'M1_TRACK_2' },
    { layer: 6, x: 180, y: 105, w: 30, h: 30, label: 'VIA1' },
    { layer: 6, x: 400, y: 225, w: 30, h: 30, label: 'VIA1' },
    { layer: 7, x: 175, y: 40, w: 40, h: 340, label: 'M2_VERTICAL_0' },
    { layer: 7, x: 395, y: 160, w: 40, h: 220, label: 'M2_VERTICAL_1' }
  ],
  pad: [
    { layer: 1, x: 60, y: 60, w: 580, h: 320, label: 'NWEL GUARD' },
    { layer: 2, x: 80, y: 80, w: 540, h: 280, label: 'GUARD RING' },
    { layer: 5, x: 120, y: 120, w: 460, h: 200, label: 'M1 METAL' },
    { layer: 6, x: 160, y: 160, w: 380, h: 120, label: 'VIA1 ARRAY' },
    { layer: 7, x: 140, y: 140, w: 420, h: 160, label: 'M2 BOND PAD' }
  ]
};

function renderLayout() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw Grid
  if (showGrid) {
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    const step = 40 * zoom;
    for (let x = panX % step; x < canvas.width; x += step) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
    }
    for (let y = panY % step; y < canvas.height; y += step) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
    }
  }

  // Draw Geometries
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;

  currentGeoms.forEach(g => {
    if (!layerVisible[g.layer]) return;
    minX = Math.min(minX, g.x);
    minY = Math.min(minY, g.y);
    maxX = Math.max(maxX, g.x + g.w);
    maxY = Math.max(maxY, g.y + g.h);

    const rx = panX + g.x * zoom * 0.7;
    const ry = panY + g.y * zoom * 0.7;
    const rw = g.w * zoom * 0.7;
    const rh = g.h * zoom * 0.7;

    ctx.fillStyle = layerColors[g.layer] || '#38bdf8';
    ctx.fillRect(rx, ry, rw, rh);
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 0.8;
    ctx.strokeRect(rx, ry, rw, rh);

    if (g.label && rw > 40) {
      ctx.fillStyle = '#ffffff';
      ctx.font = '10px monospace';
      ctx.fillText(g.label, rx + 4, ry + 12);
    }
  });

  // Draw Bounding Box
  if (showBBox && minX !== Infinity) {
    const bx = panX + minX * zoom * 0.7;
    const by = panY + minY * zoom * 0.7;
    const bw = (maxX - minX) * zoom * 0.7;
    const bh = (maxY - minY) * zoom * 0.7;
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([5, 5]);
    ctx.strokeRect(bx, by, bw, bh);
    ctx.setLineDash([]);
    ctx.fillStyle = '#f59e0b';
    ctx.font = '11px monospace';
    ctx.fillText(`BBox: [${minX} ${minY} ${maxX} ${maxY}]`, bx + 4, by - 4);
    document.getElementById('coordOverlay').innerText = 
      `BBox: [${minX} ${minY} ${maxX} ${maxY}] | Entities: ${currentGeoms.length} | Zoom: ${(zoom*100).toFixed(0)}%`;
  }
}

function loadLayoutPreset(name) {
  currentGeoms = cellPresets[name] ? [...cellPresets[name]] : [];
  renderLayout();
  document.getElementById('layoutCmdLog').innerText = `Loaded preset: ${name} with ${currentGeoms.length} shapes.`;
}

function toggleLayer(layer, vis) {
  layerVisible[layer] = vis;
  renderLayout();
}

function zoomCanvas(factor) {
  zoom = Math.max(0.4, Math.min(3.0, zoom * factor));
  renderLayout();
}

function resetCanvas() {
  zoom = 1.0; panX = 120; panY = 70;
  renderLayout();
}

function toggleGrid() {
  showGrid = !showGrid;
  document.getElementById('gridToggleBtn').innerText = 'Grid: ' + (showGrid ? 'ON' : 'OFF');
  renderLayout();
}

function toggleBBox() {
  showBBox = !showBBox;
  document.getElementById('bboxToggleBtn').innerText = 'BBox: ' + (showBBox ? 'ON' : 'OFF');
  renderLayout();
}

function executeLayoutCmd() {
  const cmd = document.getElementById('tclLayoutCmdInput').value.trim();
  const log = document.getElementById('layoutCmdLog');
  const m = cmd.match(/create\\s+box\\s+(\\w+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)/i);
  if (m) {
    const layer = parseInt(m[2]);
    const x1 = parseInt(m[3]), y1 = parseInt(m[4]), x2 = parseInt(m[5]), y2 = parseInt(m[6]);
    currentGeoms.push({ layer, x: x1, y: y1, w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), label: `L${layer}_BOX` });
    renderLayout();
    log.innerText = `[DRV-Lite Engine]: Successfully created box on layer ${layer} [${x1} ${y1} ${x2} ${y2}].`;
  } else {
    log.innerText = `[Syntax]: Use format -> $L create box TOP <layer> <x1> <y1> <x2> <y2>`;
  }
}

canvas.addEventListener('mousemove', e => {
  const rect = canvas.getBoundingClientRect();
  const mx = (e.clientX - rect.left - panX) / (zoom * 0.7);
  const my = (e.clientY - rect.top - panY) / (zoom * 0.7);
  document.getElementById('coordOverlay').innerText = 
    `Cursor: X: ${mx.toFixed(1)} um, Y: ${my.toFixed(1)} um | Zoom: ${(zoom*100).toFixed(0)}%`;
});

window.addEventListener('DOMContentLoaded', () => loadLayoutPreset('inv'));
</script>
"""
    zh_content = (en_content
        .replace("# 📐 Interactive VLSI Layout Visualizer (DRV-Lite Simulator)", "# 📐 交互式 VLSI 版图可视化仿真器 (DRV-Lite Simulator)")
        .replace("A real-time in-browser semiconductor layout visualizer inspired by Capeur's pure-Tcl **DRV-Lite** engine. Inspect multi-layer IC cell geometries, toggle metal routing tracks, observe bounding box snaps, and execute Tcl layout commands directly in the browser!",
                 "基于 Capeur 纯 Tcl 实现的 **DRV-Lite** 核心版图对象模型，本工具提供浏览器内实时 2D 半导体版图渲染与交互。支持查看多层 IC 几何体、切换金属布线层、检查包围盒坐标（Bounding Box），并可在底部直接运行纯 Tcl 版图创建命令！")
        .replace("Cell Preset:", "单元预设:")
        .replace("CMOS Inverter (INV_X1)", "CMOS 反相器 (INV_X1)")
        .replace("2-Input NAND (NAND2_X1)", "2输入与非门 (NAND2_X1)")
        .replace("M1/M2 Cross-Routing with VIA1", "M1/M2 跨层布线与 VIA1 通孔")
        .replace("I/O Bond Pad & Guard Ring", "I/O 压焊盘与保护环 (Guard Ring)")
        .replace("Layers:", "图层列表:")
        .replace("⚡ Execute Tcl Command", "⚡ 执行 Tcl 布局命令")
        .replace("DRV-Lite Pure-Tcl Engine", "DRV-Lite 纯 Tcl 引擎")
        .replace("Zero Commercial License", "零商业许可依赖")
        .replace("Interactive 2D Canvas", "HTML5 2D 交互画布")
        .replace("GDS II / OASIS Ready", "支持 GDS II / OASIS")
    )
    ms_content = (en_content
        .replace("# 📐 Interactive VLSI Layout Visualizer (DRV-Lite Simulator)", "# 📐 Visualiser Interaktif Susun Atur VLSI (Simulator DRV-Lite)")
        .replace("A real-time in-browser semiconductor layout visualizer inspired by Capeur's pure-Tcl **DRV-Lite** engine. Inspect multi-layer IC cell geometries, toggle metal routing tracks, observe bounding box snaps, and execute Tcl layout commands directly in the browser!",
                 "Visualiser susun atur semikonduktor masa nyata dalam pelayar yang diinspirasikan oleh enjin tulin Tcl **DRV-Lite** Capeur. Periksa geometri sel IC berbilang lapisan, togol laluan penghalaan logam, perhatikan kotak sempadan (Bounding Box), dan jalankan perintah susun atur Tcl terus dalam pelayar!")
        .replace("Cell Preset:", "Pratetap Sel:")
        .replace("CMOS Inverter (INV_X1)", "Penyongsang CMOS (INV_X1)")
        .replace("2-Input NAND (NAND2_X1)", "NAND 2-Input (NAND2_X1)")
        .replace("M1/M2 Cross-Routing with VIA1", "Penghalaan Silang M1/M2 dengan VIA1")
        .replace("I/O Bond Pad & Guard Ring", "Pad Ikatan I/O & Cincin Pengawal")
        .replace("Layers:", "Lapisan:")
        .replace("⚡ Execute Tcl Command", "⚡ Jalankan Perintah Tcl")
        .replace("DRV-Lite Pure-Tcl Engine", "Enjin Tulin Tcl DRV-Lite")
        .replace("Zero Commercial License", "Sifar Lesen Komersial")
        .replace("Interactive 2D Canvas", "Kanvas 2D Interaktif")
        .replace("GDS II / OASIS Ready", "Sedia GDS II / OASIS")
    )
    fr_content = (en_content
        .replace("# 📐 Interactive VLSI Layout Visualizer (DRV-Lite Simulator)", "# 📐 Visualiseur Interactif de Layout VLSI (Simulateur DRV-Lite)")
        .replace("A real-time in-browser semiconductor layout visualizer inspired by Capeur's pure-Tcl **DRV-Lite** engine. Inspect multi-layer IC cell geometries, toggle metal routing tracks, observe bounding box snaps, and execute Tcl layout commands directly in the browser!",
                 "Visualiseur de layout de semi-conducteurs en temps réel dans le navigateur, inspiré par le moteur **DRV-Lite** en pur Tcl de Capeur. Inspectez les géométries multicouches de cellules CI, basculez les pistes de routage métallique, observez les boîtes englobantes et exécutez des commandes de layout Tcl directement dans le navigateur !")
        .replace("Cell Preset:", "Préréglage Cellule :")
        .replace("CMOS Inverter (INV_X1)", "Inverseur CMOS (INV_X1)")
        .replace("2-Input NAND (NAND2_X1)", "NAND à 2 Entrées (NAND2_X1)")
        .replace("M1/M2 Cross-Routing with VIA1", "Routage Croisé M1/M2 avec VIA1")
        .replace("I/O Bond Pad & Guard Ring", "Plot de Connexion I/O & Anneau de Garde")
        .replace("Layers:", "Couches :")
        .replace("⚡ Execute Tcl Command", "⚡ Exécuter Commande Tcl")
        .replace("DRV-Lite Pure-Tcl Engine", "Moteur Pur Tcl DRV-Lite")
        .replace("Zero Commercial License", "Zéro Licence Commerciale")
        .replace("Interactive 2D Canvas", "Canevas 2D Interactif")
        .replace("GDS II / OASIS Ready", "Prêt GDS II / OASIS")
    )
    (DOCS / "help" / "layout_viewer.md").write_text(en_content, encoding="utf-8")
    (DOCS / "help" / "layout_viewer.zh.md").write_text(zh_content, encoding="utf-8")
    (DOCS / "help" / "layout_viewer.ms.md").write_text(ms_content, encoding="utf-8")
    (DOCS / "help" / "layout_viewer.fr.md").write_text(fr_content, encoding="utf-8")


def write_timing_calculator_pages() -> None:
    (DOCS / "help").mkdir(parents=True, exist_ok=True)
    en_content = """# ⚡ Interactive STA Timing Slack & WNS/TNS Gatekeeper

<div class="tcl-badge-cluster">
  <span class="tcl-badge blue">Static Timing Analysis (STA)</span>
  <span class="tcl-badge green">Worst Negative Slack (WNS)</span>
  <span class="tcl-badge purple">Total Negative Slack (TNS)</span>
  <span class="tcl-badge amber">Tapeout Sign-Off Gatekeeper</span>
</div>

Interactive digital IC timing sign-off simulator. Adjust clock parameters, wire delays, setup times, and uncertainty to observe Slack calculations in real time, visualize timing margin gauges, and test tapeout pass/fail criteria!

---

<div class="timing-calculator-container" style="background: var(--tcl-surface); border: 1px solid var(--tcl-border); border-radius: 12px; padding: 24px; margin: 24px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
  
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px;">
    <!-- Sliders Column -->
    <div>
      <h3 style="margin-top:0; font-size:16px;">⏱️ Timing Constraints & Delays</h3>
      
      <div style="margin-bottom: 14px;">
        <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:600;">
          <span>Target Clock Period ($T_{clk}$):</span>
          <span id="val_clk" style="color:var(--tcl-blue-600);">1.00 ns (1000 MHz)</span>
        </div>
        <input type="range" id="input_clk" min="0.5" max="3.0" step="0.05" value="1.0" oninput="recalcTiming()" style="width:100%; cursor:pointer;">
      </div>

      <div style="margin-bottom: 14px;">
        <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:600;">
          <span>Data Path Delay ($T_{data}$):</span>
          <span id="val_data" style="color:var(--tcl-blue-600);">720 ps</span>
        </div>
        <input type="range" id="input_data" min="200" max="1600" step="10" value="720" oninput="recalcTiming()" style="width:100%; cursor:pointer;">
      </div>

      <div style="margin-bottom: 14px;">
        <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:600;">
          <span>Clock-to-Q Delay ($T_{clk-q}$):</span>
          <span id="val_clk_q" style="color:var(--tcl-blue-600);">90 ps</span>
        </div>
        <input type="range" id="input_clk_q" min="20" max="250" step="5" value="90" oninput="recalcTiming()" style="width:100%; cursor:pointer;">
      </div>

      <div style="margin-bottom: 14px;">
        <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:600;">
          <span>Library Setup Time ($T_{setup}$):</span>
          <span id="val_setup" style="color:var(--tcl-blue-600);">50 ps</span>
        </div>
        <input type="range" id="input_setup" min="10" max="150" step="5" value="50" oninput="recalcTiming()" style="width:100%; cursor:pointer;">
      </div>

      <div style="margin-bottom: 14px;">
        <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:600;">
          <span>Clock Uncertainty / Jitter ($T_{unc}$):</span>
          <span id="val_unc" style="color:var(--tcl-blue-600);">40 ps</span>
        </div>
        <input type="range" id="input_unc" min="0" max="150" step="5" value="40" oninput="recalcTiming()" style="width:100%; cursor:pointer;">
      </div>
    </div>

    <!-- Live Equation & Verdict Column -->
    <div style="background: var(--md-default-bg-color); border: 1px solid var(--tcl-border); border-radius: 10px; padding: 20px; display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <h3 style="margin-top:0; font-size:16px;">📊 Setup Slack Equation</h3>
        <div style="font-family:monospace; font-size:12px; background:var(--tcl-surface); padding:10px; border-radius:6px; line-height:1.6; border:1px solid var(--tcl-border);">
          <div>Required = T_clk - T_unc - T_setup = <span id="eq_req">910 ps</span></div>
          <div>Arrival  = T_clk_q + T_data       = <span id="eq_arr">810 ps</span></div>
          <div style="border-top:1px dashed var(--tcl-border); margin-top:6px; padding-top:6px; font-weight:bold; font-size:13px;">
            Slack = Required - Arrival = <span id="eq_slack" style="color:#10b981;">+100 ps (+0.100 ns)</span>
          </div>
        </div>

        <!-- Animated Gauge Bar -->
        <div style="margin-top: 18px;">
          <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px; font-weight:600;">
            <span>Timing Margin Gauge:</span>
            <span id="gaugeStatusText" style="color:#10b981;">Positive Slack (+100 ps)</span>
          </div>
          <div style="width:100%; height:14px; background:rgba(0,0,0,0.1); border-radius:7px; overflow:hidden; position:relative;">
            <div id="gaugeBar" style="width:65%; height:100%; background:#10b981; transition:all 0.2s ease;"></div>
          </div>
        </div>
      </div>

      <!-- Verdict Stamp -->
      <div id="signoffStamp" style="margin-top:20px; padding:16px; border-radius:8px; text-align:center; font-weight:800; font-size:15px; background:rgba(16, 185, 129, 0.12); color:#10b981; border:2px solid #10b981; letter-spacing:0.5px;">
        🛡️ TIMING MET · APPROVED FOR TAPEOUT
      </div>
    </div>
  </div>

  <!-- Multi-Path Scenario Table -->
  <div style="margin-top: 24px;">
    <h3 style="font-size:15px; margin-bottom:10px;">📋 Multi-Path Sign-off Summary (Critical Path Group)</h3>
    <table style="width:100%; font-size:13px; border-collapse:collapse;">
      <thead>
        <tr style="background:var(--md-default-bg-color); text-align:left;">
          <th style="padding:8px 12px; border:1px solid var(--tcl-border);">Path Endpoint</th>
          <th style="padding:8px 12px; border:1px solid var(--tcl-border);">Data Delay</th>
          <th style="padding:8px 12px; border:1px solid var(--tcl-border);">Arrival</th>
          <th style="padding:8px 12px; border:1px solid var(--tcl-border);">Slack</th>
          <th style="padding:8px 12px; border:1px solid var(--tcl-border);">Status</th>
        </tr>
      </thead>
      <tbody id="multiPathTable">
        <!-- Rendered dynamically -->
      </tbody>
    </table>
    <div style="margin-top:10px; display:flex; gap:20px; font-size:13px; font-family:monospace; font-weight:bold;">
      <span>WNS (Worst Negative Slack): <span id="summary_wns" style="color:#10b981;">0.000 ns</span></span>
      <span>TNS (Total Negative Slack): <span id="summary_tns" style="color:#10b981;">0.000 ns</span></span>
    </div>
  </div>
</div>

<script>
function recalcTiming() {
  const t_clk = parseFloat(document.getElementById('input_clk').value) * 1000;
  const t_data = parseFloat(document.getElementById('input_data').value);
  const t_clk_q = parseFloat(document.getElementById('input_clk_q').value);
  const t_setup = parseFloat(document.getElementById('input_setup').value);
  const t_unc = parseFloat(document.getElementById('input_unc').value);

  document.getElementById('val_clk').innerText = (t_clk / 1000).toFixed(2) + ' ns (' + (1000000 / t_clk).toFixed(0) + ' MHz)';
  document.getElementById('val_data').innerText = t_data.toFixed(0) + ' ps';
  document.getElementById('val_clk_q').innerText = t_clk_q.toFixed(0) + ' ps';
  document.getElementById('val_setup').innerText = t_setup.toFixed(0) + ' ps';
  document.getElementById('val_unc').innerText = t_unc.toFixed(0) + ' ps';

  const req = t_clk - t_unc - t_setup;
  const arr = t_clk_q + t_data;
  const slack = req - arr;

  document.getElementById('eq_req').innerText = req.toFixed(0) + ' ps';
  document.getElementById('eq_arr').innerText = arr.toFixed(0) + ' ps';
  
  const slackElem = document.getElementById('eq_slack');
  const stamp = document.getElementById('signoffStamp');
  const bar = document.getElementById('gaugeBar');
  const gaugeText = document.getElementById('gaugeStatusText');

  if (slack >= 0) {
    slackElem.innerText = `+${slack.toFixed(0)} ps (+${(slack/1000).toFixed(3)} ns)`;
    slackElem.style.color = '#10b981';
    gaugeText.innerText = `Positive Slack (+${slack.toFixed(0)} ps)`;
    gaugeText.style.color = '#10b981';
    bar.style.background = '#10b981';
    bar.style.width = Math.min(100, Math.max(10, (slack / 500) * 100)) + '%';
    stamp.innerHTML = '🛡️ TIMING MET · APPROVED FOR TAPEOUT';
    stamp.style.color = '#10b981';
    stamp.style.borderColor = '#10b981';
    stamp.style.background = 'rgba(16, 185, 129, 0.12)';
  } else {
    slackElem.innerText = `${slack.toFixed(0)} ps (${(slack/1000).toFixed(3)} ns)`;
    slackElem.style.color = '#ef4444';
    gaugeText.innerText = `TIMING VIOLATION (${slack.toFixed(0)} ps)`;
    gaugeText.style.color = '#ef4444';
    bar.style.background = '#ef4444';
    bar.style.width = Math.min(100, Math.max(15, (Math.abs(slack) / 500) * 100)) + '%';
    stamp.innerHTML = '⚠️ TIMING VIOLATION · TAPEOUT GATE BLOCKED';
    stamp.style.color = '#ef4444';
    stamp.style.borderColor = '#ef4444';
    stamp.style.background = 'rgba(239, 68, 68, 0.12)';
  }

  // Update multi-path scenarios
  updateMultiPaths(req, t_clk_q);
}

function updateMultiPaths(req, clk_q) {
  const paths = [
    { name: 'u_alu/adder_reg_31/D', data: 720 },
    { name: 'u_fsm/state_next_reg/D', data: 540 },
    { name: 'u_cache/tag_match_reg/D', data: 890 },
    { name: 'u_mmu/tlb_hit_reg/D', data: 630 },
    { name: 'u_io/uart_tx_shift_reg/D', data: 410 }
  ];

  let wns = 0, tns = 0;
  let rows = '';

  paths.forEach(p => {
    const arr = clk_q + p.data;
    const slack = (req - arr) / 1000;
    if (slack < 0) {
      wns = Math.min(wns, slack);
      tns += slack;
    }
    const isMet = slack >= 0;
    rows += `<tr>
      <td style="padding:6px 12px; border:1px solid var(--tcl-border); font-family:monospace;">${p.name}</td>
      <td style="padding:6px 12px; border:1px solid var(--tcl-border);">${p.data} ps</td>
      <td style="padding:6px 12px; border:1px solid var(--tcl-border);">${arr.toFixed(0)} ps</td>
      <td style="padding:6px 12px; border:1px solid var(--tcl-border); font-weight:bold; color:${isMet ? '#10b981':'#ef4444'};">${slack >= 0 ? '+':''}${slack.toFixed(3)} ns</td>
      <td style="padding:6px 12px; border:1px solid var(--tcl-border);"><span style="display:inline-block; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:bold; background:${isMet ? 'rgba(16,185,129,0.15)':'rgba(239,68,68,0.15)'}; color:${isMet ? '#10b981':'#ef4444'};">${isMet ? 'PASS':'VIOLATION'}</span></td>
    </tr>`;
  });

  document.getElementById('multiPathTable').innerHTML = rows;
  const wnsElem = document.getElementById('summary_wns');
  const tnsElem = document.getElementById('summary_tns');
  wnsElem.innerText = wns.toFixed(3) + ' ns';
  tnsElem.innerText = tns.toFixed(3) + ' ns';
  wnsElem.style.color = wns < 0 ? '#ef4444' : '#10b981';
  tnsElem.style.color = tns < 0 ? '#ef4444' : '#10b981';
}

window.addEventListener('DOMContentLoaded', recalcTiming);
</script>
"""
    zh_content = (en_content
        .replace("# ⚡ Interactive STA Timing Slack & WNS/TNS Gatekeeper", "# ⚡ 交互式 STA 静态时序 Slack 与 WNS/TNS 签核门禁")
        .replace("Interactive digital IC timing sign-off simulator. Adjust clock parameters, wire delays, setup times, and uncertainty to observe Slack calculations in real time, visualize timing margin gauges, and test tapeout pass/fail criteria!",
                 "数字芯片时序签核交互仿真器。实时调节目标时钟周期、数据路径组合延迟、触发器固有延迟与时钟不确定度（Uncertainty），直观观察建立时间裕量（Setup Slack）动态计算、观察时序安全仪表盘，并自动化检验流片准入判决（Tapeout Gate Verdict）！")
        .replace("Static Timing Analysis (STA)", "静态时序分析 (STA)")
        .replace("Worst Negative Slack (WNS)", "最差负裕量 (WNS)")
        .replace("Total Negative Slack (TNS)", "总负裕量 (TNS)")
        .replace("Tapeout Sign-Off Gatekeeper", "流片签核自动化门禁")
        .replace("⏱️ Timing Constraints & Delays", "⏱️ 时序约束与延迟参数")
        .replace("Target Clock Period ($T_{clk}$):", "目标时钟周期 ($T_{clk}$):")
        .replace("Data Path Delay ($T_{data}$):", "数据路径延迟 ($T_{data}$):")
        .replace("Clock-to-Q Delay ($T_{clk-q}$):", "触发器时钟到输出延迟 ($T_{clk-q}$):")
        .replace("Library Setup Time ($T_{setup}$):", "器件库建立时间 ($T_{setup}$):")
        .replace("Clock Uncertainty / Jitter ($T_{unc}$):", "时钟不确定度与抖动 ($T_{unc}$):")
        .replace("📊 Setup Slack Equation", "📊 建立时间裕量方程")
        .replace("Timing Margin Gauge:", "时序安全仪表盘:")
        .replace("📋 Multi-Path Sign-off Summary (Critical Path Group)", "📋 多路径签核汇总表 (关键时序路径)")
        .replace("Path Endpoint", "路径终点")
        .replace("Data Delay", "数据延迟")
        .replace("Arrival", "到达时间")
        .replace("Status", "状态")
    )
    ms_content = (en_content
        .replace("# ⚡ Interactive STA Timing Slack & WNS/TNS Gatekeeper", "# ⚡ Penjaga Masa STA Interaktif: Slack & WNS/TNS Sign-Off")
        .replace("Interactive digital IC timing sign-off simulator. Adjust clock parameters, wire delays, setup times, and uncertainty to observe Slack calculations in real time, visualize timing margin gauges, and test tapeout pass/fail criteria!",
                 "Simulator sign-off pemasaan IC digital interaktif. Laraskan parameter jam, kelewatan wayar, masa persediaan (Setup), dan ketidakpastian (Uncertainty) untuk melihat pengiraan Slack secara masa nyata, memvisualisasikan tolok margin pemasaan, dan menguji kriteria lulus/gagal tapeout!")
        .replace("Static Timing Analysis (STA)", "Analisis Pemasaan Statik (STA)")
        .replace("Worst Negative Slack (WNS)", "Slack Negatif Terburuk (WNS)")
        .replace("Total Negative Slack (TNS)", "Jumlah Slack Negatif (TNS)")
        .replace("Tapeout Sign-Off Gatekeeper", "Penjaga Pintu Tapeout Sign-Off")
        .replace("⏱️ Timing Constraints & Delays", "⏱️ Kekangan Pemasaan & Kelewatan")
        .replace("Target Clock Period ($T_{clk}$):", "Tempoh Jam Sasaran ($T_{clk}$):")
        .replace("Data Path Delay ($T_{data}$):", "Kelewatan Laluan Data ($T_{data}$):")
        .replace("Clock-to-Q Delay ($T_{clk-q}$):", "Kelewatan Jam-ke-Q ($T_{clk-q}$):")
        .replace("Library Setup Time ($T_{setup}$):", "Masa Persediaan Pustaka ($T_{setup}$):")
        .replace("Clock Uncertainty / Jitter ($T_{unc}$):", "Ketidakpastian Jam / Jitter ($T_{unc}$):")
        .replace("📊 Setup Slack Equation", "📊 Persamaan Setup Slack")
        .replace("Timing Margin Gauge:", "Tolok Margin Pemasaan:")
        .replace("📋 Multi-Path Sign-off Summary (Critical Path Group)", "📋 Ringkasan Sign-off Pelbagai Laluan (Kumpulan Laluan Kritikal)")
        .replace("Path Endpoint", "Titik Akhir Laluan")
        .replace("Data Delay", "Kelewatan Data")
        .replace("Arrival", "Ketibaan")
        .replace("Status", "Status")
    )
    fr_content = (en_content
        .replace("# ⚡ Interactive STA Timing Slack & WNS/TNS Gatekeeper", "# ⚡ Contrôleur Temporel STA Interactif : Marge Slack & WNS/TNS")
        .replace("Interactive digital IC timing sign-off simulator. Adjust clock parameters, wire delays, setup times, and uncertainty to observe Slack calculations in real time, visualize timing margin gauges, and test tapeout pass/fail criteria!",
                 "Simulateur interactif de validation temporelle pour circuits intégrés numériques. Ajustez la période d'horloge, les délais de propagation, les temps d'établissement (Setup) et l'incertitude d'horloge pour observer le calcul de Slack en temps réel, visualiser la jauge de marge et vérifier les critères de validation finale (Tapeout) !")
        .replace("Static Timing Analysis (STA)", "Analyse Temporelle Statique (STA)")
        .replace("Worst Negative Slack (WNS)", "Pire Marge Négative (WNS)")
        .replace("Total Negative Slack (TNS)", "Marge Négative Totale (TNS)")
        .replace("Tapeout Sign-Off Gatekeeper", "Porte de Validation Tapeout")
        .replace("⏱️ Timing Constraints & Delays", "⏱️ Contraintes Temporelles & Délais")
        .replace("Target Clock Period ($T_{clk}$):", "Période d'Horloge Cible ($T_{clk}$):")
        .replace("Data Path Delay ($T_{data}$):", "Délai du Chemin de Données ($T_{data}$):")
        .replace("Clock-to-Q Delay ($T_{clk-q}$):", "Délai Horloge-vers-Q ($T_{clk-q}$):")
        .replace("Library Setup Time ($T_{setup}$):", "Temps d'Établissement Bibliothèque ($T_{setup}$):")
        .replace("Clock Uncertainty / Jitter ($T_{unc}$):", "Incertitude d'Horloge / Gigue ($T_{unc}$):")
        .replace("📊 Setup Slack Equation", "📊 Équation de Setup Slack")
        .replace("Timing Margin Gauge:", "Jauge de Marge Temporelle :")
        .replace("📋 Multi-Path Sign-off Summary (Critical Path Group)", "📋 Tableau Récapitulatif Multi-Chemins (Chemins Critiques)")
        .replace("Path Endpoint", "Point d'Arrivée")
        .replace("Data Delay", "Délai Données")
        .replace("Arrival", "Arrivée")
        .replace("Status", "Statut")
    )
    (DOCS / "help" / "timing_calculator.md").write_text(en_content, encoding="utf-8")
    (DOCS / "help" / "timing_calculator.zh.md").write_text(zh_content, encoding="utf-8")
    (DOCS / "help" / "timing_calculator.ms.md").write_text(ms_content, encoding="utf-8")
    (DOCS / "help" / "timing_calculator.fr.md").write_text(fr_content, encoding="utf-8")


def write_stylesheets() -> None:
    css_dir = DOCS / "stylesheets"
    css_dir.mkdir(parents=True, exist_ok=True)
    css_content = """/* Modern High-Readability Semiconductor Engineering Design System */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root, [data-md-color-scheme="default"] {
  /* Modern High-Readability Light Palette */
  --md-default-bg-color: #ffffff !important;
  --md-default-bg-color--light: #f8fafc !important;
  --md-default-bg-color--lighter: #f1f5f9 !important;
  --md-default-fg-color: #0f172a !important;       /* Slate 900 */
  --md-default-fg-color--light: #1e293b !important; /* Slate 800 body text */
  --md-default-fg-color--lighter: #475569 !important; /* Slate 600 */
  
  --md-primary-fg-color: #0f172a !important;       /* Slate 900 Header */
  --md-primary-fg-color--light: #1e293b !important;
  --md-primary-fg-color--dark: #020617 !important;
  --md-accent-fg-color: #2563eb !important;        /* Royal Blue */
  --md-code-bg-color: #0f172a !important;
  --md-code-fg-color: #f8fafc !important;

  /* Code Syntax Highlighting Tokens */
  --md-code-hl-color: #38bdf8 !important;
  --md-code-hl-number-color: #fb923c !important;
  --md-code-hl-special-color: #f87171 !important;
  --md-code-hl-function-color: #60a5fa !important;
  --md-code-hl-constant-color: #c084fc !important;
  --md-code-hl-keyword-color: #818cf8 !important;
  --md-code-hl-string-color: #4ade80 !important;
  --md-code-hl-name-color: #f8fafc !important;
  --md-code-hl-operator-color: #94a3b8 !important;
  --md-code-hl-punctuation-color: #cbd5e1 !important;
  --md-code-hl-comment-color: #94a3b8 !important;
  --md-code-hl-generic-color: #cbd5e1 !important;
  --md-code-hl-variable-color: #e2e8f0 !important;

  --tcl-blue-600: #2563eb;
  --tcl-blue-700: #1d4ed8;
  --tcl-surface: #f8fafc;
  --tcl-surface-card: #ffffff;
  --tcl-border: #e2e8f0;
  --tcl-border-hover: #cbd5e1;
  --tcl-heading: #0f172a;
}

[data-md-color-scheme="slate"] {
  /* OLED Midnight High-Readability Dark Palette */
  --md-default-bg-color: #0b0f19 !important;       /* Deep space slate */
  --md-default-bg-color--light: #111827 !important;
  --md-default-bg-color--lighter: #1e293b !important;
  --md-default-fg-color: #f8fafc !important;       /* Slate 50 */
  --md-default-fg-color--light: #cbd5e1 !important; /* Slate 300 body text */
  --md-default-fg-color--lighter: #94a3b8 !important; /* Slate 400 */

  --md-primary-fg-color: #090d16 !important;
  --md-primary-fg-color--light: #111827 !important;
  --md-primary-fg-color--dark: #030712 !important;
  --md-accent-fg-color: #38bdf8 !important;        /* Electric Cyan */
  --md-code-bg-color: #070a12 !important;
  --md-code-fg-color: #f1f5f9 !important;

  /* Code Syntax Highlighting Tokens */
  --md-code-hl-color: #38bdf8 !important;
  --md-code-hl-number-color: #fb923c !important;
  --md-code-hl-special-color: #f87171 !important;
  --md-code-hl-function-color: #60a5fa !important;
  --md-code-hl-constant-color: #c084fc !important;
  --md-code-hl-keyword-color: #818cf8 !important;
  --md-code-hl-string-color: #4ade80 !important;
  --md-code-hl-name-color: #f1f5f9 !important;
  --md-code-hl-operator-color: #94a3b8 !important;
  --md-code-hl-punctuation-color: #cbd5e1 !important;
  --md-code-hl-comment-color: #94a3b8 !important;
  --md-code-hl-generic-color: #cbd5e1 !important;
  --md-code-hl-variable-color: #e2e8f0 !important;

  --tcl-blue-600: #38bdf8;
  --tcl-blue-700: #60a5fa;
  --tcl-surface: #111827;
  --tcl-surface-card: #1e293b;
  --tcl-border: #334155;
  --tcl-border-hover: #475569;
  --tcl-heading: #f8fafc;
}

/* Global Typography - Pure Sans-Serif Stack (No fuzzy serifs!) */
body, .md-typeset {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
  font-size: 15.5px;
  line-height: 1.75;
  color: var(--md-default-fg-color--light);
  background-color: var(--md-default-bg-color);
  -webkit-font-smoothing: antialiased;
}

.md-typeset p, .md-typeset li {
  color: var(--md-default-fg-color--light) !important;
}

.md-typeset strong {
  color: var(--tcl-heading) !important;
  font-weight: 700 !important;
}

.md-typeset h1, .md-typeset h2, .md-typeset h3, .md-typeset h4 {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  color: var(--tcl-heading) !important;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.md-typeset code, .md-typeset pre {
  font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, monospace !important;
}

/* Explicit Inline Code Styling */
.md-typeset :not(pre) > code {
  color: #0f172a !important;
  background-color: #f1f5f9 !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 4px !important;
  padding: 0.18em 0.45em !important;
  font-size: 0.88em !important;
  font-weight: 600 !important;
}
[data-md-color-scheme="slate"] .md-typeset :not(pre) > code {
  color: #f1f5f9 !important;
  background-color: #1e293b !important;
  border-color: #334155 !important;
}

/* Code Blocks - High-Contrast Syntax Highlighting */
.md-typeset pre > code {
  color: #f8fafc !important;
  background-color: #0f172a !important;
}

.md-typeset .highlight pre {
  background-color: #0f172a !important;
  border: 1px solid #1e293b !important;
  border-radius: 8px !important;
}

/* Crystal-Clear Comments - High Contrast Slate 400 */
.md-typeset .highlight .c,
.md-typeset .highlight .c1,
.md-typeset .highlight .ch,
.md-typeset .highlight .cm,
.md-typeset .highlight .cp,
.md-typeset .highlight .cpf,
.md-typeset .highlight .cs,
.md-typeset .highlight .sd {
  color: #94a3b8 !important; /* Silvery Slate 400 - High Contrast (7:1) */
  font-style: italic !important;
}

/* Enhanced Code Tokens */
.md-typeset .highlight .k,
.md-typeset .highlight .kd,
.md-typeset .highlight .kn,
.md-typeset .highlight .kp,
.md-typeset .highlight .kr,
.md-typeset .highlight .kt {
  color: #c084fc !important; /* Violet Keyword */
}

.md-typeset .highlight .nb,
.md-typeset .highlight .bp {
  color: #818cf8 !important; /* Built-in */
}

.md-typeset .highlight .nc,
.md-typeset .highlight .ne,
.md-typeset .highlight .nf,
.md-typeset .highlight .nn {
  color: #60a5fa !important; /* Function name */
}

.md-typeset .highlight .s,
.md-typeset .highlight .s1,
.md-typeset .highlight .s2,
.md-typeset .highlight .sb,
.md-typeset .highlight .sc,
.md-typeset .highlight .si,
.md-typeset .highlight .sx {
  color: #4ade80 !important; /* String */
}

.md-typeset .highlight .m,
.md-typeset .highlight .mb,
.md-typeset .highlight .mf,
.md-typeset .highlight .mh,
.md-typeset .highlight .mi,
.md-typeset .highlight .mo {
  color: #fb923c !important; /* Number */
}

.md-typeset .highlight .o,
.md-typeset .highlight .ow {
  color: #38bdf8 !important; /* Operator */
}

.md-typeset .highlight .p {
  color: #cbd5e1 !important; /* Punctuation */
}

.md-typeset .highlight .na,
.md-typeset .highlight .nv,
.md-typeset .highlight .vc,
.md-typeset .highlight .vg,
.md-typeset .highlight .vi {
  color: #f1f5f9 !important; /* Variables */
}

/* High Contrast Links - Target standard prose links only */
.md-typeset p a,
.md-typeset li a,
.md-typeset td a,
.md-typeset dd a {
  color: #2563eb;
  font-weight: 500;
  text-decoration: underline;
  text-underline-offset: 3px;
  text-decoration-color: rgba(37, 99, 235, 0.35);
  transition: color 0.15s, text-decoration-color 0.15s;
}
.md-typeset p a:hover,
.md-typeset li a:hover,
.md-typeset td a:hover,
.md-typeset dd a:hover {
  color: #1d4ed8;
  text-decoration-color: #1d4ed8;
}
[data-md-color-scheme="slate"] .md-typeset p a,
[data-md-color-scheme="slate"] .md-typeset li a,
[data-md-color-scheme="slate"] .md-typeset td a,
[data-md-color-scheme="slate"] .md-typeset dd a {
  color: #38bdf8;
  text-decoration-color: rgba(56, 189, 248, 0.35);
}
[data-md-color-scheme="slate"] .md-typeset p a:hover,
[data-md-color-scheme="slate"] .md-typeset li a:hover,
[data-md-color-scheme="slate"] .md-typeset td a:hover,
[data-md-color-scheme="slate"] .md-typeset dd a:hover {
  color: #7dd3fc;
  text-decoration-color: #7dd3fc;
}

/* Header & Tabs */
.md-header {
  background-color: #0f172a !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.12) !important;
}

.md-tabs {
  background-color: #1e293b !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
}

.md-tabs__link {
  font-weight: 500;
  font-size: 14px;
  opacity: 0.85;
}

.md-tabs__link--active {
  opacity: 1 !important;
  font-weight: 600 !important;
  color: #38bdf8 !important;
}

/* Hero Section */
.tcl-hero {
  padding: 36px 0 24px;
  border-bottom: 1px solid var(--tcl-border);
  margin-bottom: 28px;
}
.tcl-badge-cluster {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.tcl-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 600;
  background: #f1f5f9;
  color: #334155;
  border: 1px solid #e2e8f0;
}
[data-md-color-scheme="slate"] .tcl-badge {
  background: #1e293b;
  color: #cbd5e1;
  border-color: #334155;
}
.tcl-badge.blue {
  background: #eff6ff;
  color: #1e40af;
  border-color: #bfdbfe;
}
[data-md-color-scheme="slate"] .tcl-badge.blue {
  background: rgba(37, 99, 235, 0.15);
  color: #93c5fd;
  border-color: rgba(96, 165, 250, 0.3);
}
.tcl-badge.amber {
  background: #fffbeb;
  color: #92400e;
  border-color: #fde68a;
}
[data-md-color-scheme="slate"] .tcl-badge.amber {
  background: rgba(245, 158, 11, 0.15);
  color: #fcd34d;
  border-color: rgba(252, 211, 77, 0.3);
}
.tcl-badge.green {
  background: #ecfdf5;
  color: #065f46;
  border-color: #a7f3d0;
}
[data-md-color-scheme="slate"] .tcl-badge.green {
  background: rgba(16, 185, 129, 0.15);
  color: #6ee7b7;
  border-color: rgba(110, 231, 183, 0.3);
}
.tcl-badge.purple {
  background: #faf5ff;
  color: #581c87;
  border-color: #e9d5ff;
}
[data-md-color-scheme="slate"] .tcl-badge.purple {
  background: rgba(168, 85, 247, 0.15);
  color: #d8b4fe;
  border-color: rgba(216, 180, 254, 0.3);
}
.tcl-badge.cyan {
  background: #ecfeff;
  color: #155e75;
  border-color: #a5f3fc;
}
[data-md-color-scheme="slate"] .tcl-badge.cyan {
  background: rgba(6, 182, 212, 0.15);
  color: #67e8f9;
  border-color: rgba(103, 232, 249, 0.3);
}

.tcl-hero-title {
  font-size: 2.3rem;
  font-weight: 800;
  line-height: 1.25;
  margin: 8px 0 16px 0;
  color: var(--tcl-heading) !important;
  letter-spacing: -0.03em;
}
.tcl-hero-subtitle {
  font-size: 1.1rem;
  line-height: 1.7;
  color: var(--md-default-fg-color--light);
  max-width: 880px;
  margin-bottom: 24px;
}

/* Hero CTA Buttons */
.tcl-cta-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
  margin: 24px 0 16px;
}
.md-typeset a.tcl-btn,
.tcl-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 22px;
  border-radius: 8px;
  font-size: 14.5px;
  font-weight: 600;
  line-height: 1.4;
  text-decoration: none !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}

/* Primary Button: High-Contrast Dark Slate */
.md-typeset a.tcl-btn-primary,
.tcl-btn-primary {
  background: #0f172a !important;
  color: #ffffff !important;
  border: 1px solid #0f172a !important;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.18);
}
.md-typeset a.tcl-btn-primary:hover,
.tcl-btn-primary:hover {
  background: #1e293b !important;
  border-color: #1e293b !important;
  color: #ffffff !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.28);
}
[data-md-color-scheme="slate"] .md-typeset a.tcl-btn-primary,
[data-md-color-scheme="slate"] .tcl-btn-primary {
  background: #38bdf8 !important;
  color: #0b0f19 !important;
  border: 1px solid #38bdf8 !important;
  box-shadow: 0 4px 14px rgba(56, 189, 248, 0.3);
}
[data-md-color-scheme="slate"] .md-typeset a.tcl-btn-primary:hover,
[data-md-color-scheme="slate"] .tcl-btn-primary:hover {
  background: #7dd3fc !important;
  color: #0b0f19 !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(56, 189, 248, 0.45);
}

/* Accent Button (Tcl Quest RPG) */
.md-typeset a.tcl-btn-accent,
.tcl-btn-accent {
  background: #f5f3ff !important;
  color: #6b21a8 !important;
  border: 1px solid #ddd6fe !important;
  box-shadow: 0 2px 6px rgba(107, 33, 168, 0.08);
}
.md-typeset a.tcl-btn-accent:hover,
.tcl-btn-accent:hover {
  background: #ede9fe !important;
  border-color: #c4b5fd !important;
  color: #581c87 !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(107, 33, 168, 0.15);
}
[data-md-color-scheme="slate"] .md-typeset a.tcl-btn-accent,
[data-md-color-scheme="slate"] .tcl-btn-accent {
  background: rgba(168, 85, 247, 0.18) !important;
  color: #e9d5ff !important;
  border: 1px solid rgba(192, 132, 252, 0.4) !important;
}
[data-md-color-scheme="slate"] .md-typeset a.tcl-btn-accent:hover,
[data-md-color-scheme="slate"] .tcl-btn-accent:hover {
  background: rgba(168, 85, 247, 0.28) !important;
  border-color: rgba(192, 132, 252, 0.6) !important;
  color: #ffffff !important;
  transform: translateY(-2px);
}

/* Secondary Button: Neutral High-End Slate Outline */
.md-typeset a.tcl-btn-secondary,
.tcl-btn-secondary {
  background: #ffffff !important;
  color: #1e293b !important;
  border: 1px solid #cbd5e1 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
.md-typeset a.tcl-btn-secondary:hover,
.tcl-btn-secondary:hover {
  background: #f8fafc !important;
  border-color: #94a3b8 !important;
  color: #0f172a !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
[data-md-color-scheme="slate"] .md-typeset a.tcl-btn-secondary,
[data-md-color-scheme="slate"] .tcl-btn-secondary {
  background: #1e293b !important;
  color: #f1f5f9 !important;
  border: 1px solid #334155 !important;
}
[data-md-color-scheme="slate"] .md-typeset a.tcl-btn-secondary:hover,
[data-md-color-scheme="slate"] .tcl-btn-secondary:hover {
  background: #334155 !important;
  border-color: #475569 !important;
  color: #ffffff !important;
  transform: translateY(-2px);
}

/* Stats Fact Strip */
.tcl-fact-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 16px;
  padding: 22px 26px;
  background: var(--tcl-surface);
  border: 1px solid var(--tcl-border);
  border-radius: 12px;
  margin: 24px 0 36px;
}
.tcl-fact-item {
  text-align: center;
}
.tcl-fact-val {
  font-family: 'Inter', sans-serif;
  font-size: 2.1rem;
  font-weight: 800;
  color: var(--tcl-heading);
  display: block;
  letter-spacing: -0.02em;
}
[data-md-color-scheme="slate"] .tcl-fact-val {
  color: #38bdf8;
}
.tcl-fact-lbl {
  font-size: 0.85rem;
  color: var(--md-default-fg-color--lighter);
  font-weight: 600;
  margin-top: 4px;
}

/* Interactive Tools Hub Grid */
.tcl-tools-section-title {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--tcl-heading);
  margin: 36px 0 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.tcl-tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin: 0 0 36px;
}
.md-typeset a.tcl-tool-card,
.tcl-tool-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 18px 20px;
  border-radius: 10px;
  border: 1px solid var(--tcl-border);
  background: var(--tcl-surface-card);
  text-decoration: none !important;
  color: var(--md-default-fg-color--light) !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}
.md-typeset a.tcl-tool-card:hover,
.tcl-tool-card:hover {
  border-color: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.08);
}
[data-md-color-scheme="slate"] .md-typeset a.tcl-tool-card:hover,
[data-md-color-scheme="slate"] .tcl-tool-card:hover {
  border-color: #38bdf8;
  box-shadow: 0 8px 20px rgba(56, 189, 248, 0.12);
}
.tcl-tool-icon {
  font-size: 1.75rem;
  line-height: 1;
  flex-shrink: 0;
  padding-top: 2px;
}
.tcl-tool-body {
  flex: 1;
  min-width: 0;
}
.tcl-tool-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--tcl-heading);
  margin-bottom: 4px;
  line-height: 1.35;
}
.tcl-tool-desc {
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--md-default-fg-color--lighter);
}
.tcl-tool-arrow {
  color: var(--md-default-fg-color--lighter);
  font-size: 1.2rem;
  font-weight: 600;
  transition: transform 0.2s ease, color 0.2s ease;
  flex-shrink: 0;
}
.md-typeset a.tcl-tool-card:hover .tcl-tool-arrow {
  transform: translateX(4px);
  color: #2563eb;
}
[data-md-color-scheme="slate"] .md-typeset a.tcl-tool-card:hover .tcl-tool-arrow {
  color: #38bdf8;
}

/* 3-Column Route Cards */
.tcl-routes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
  gap: 20px;
  margin: 20px 0 36px;
}
.tcl-route-card {
  padding: 26px;
  border-radius: 12px;
  border: 1px solid var(--tcl-border);
  background: var(--tcl-surface-card);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: hidden;
  transition: all 0.25s ease;
}
.tcl-route-card:hover {
  transform: translateY(-3px);
  border-color: #2563eb;
  box-shadow: 0 12px 28px rgba(37, 99, 235, 0.12);
}
.tcl-route-card::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 4px;
  background: #2563eb;
}
.tcl-route-card.route-exp::before { background: #f59e0b; }
.tcl-route-card.route-vlsi::before { background: #06b6d4; }
.tcl-route-num {
  font-size: 11px;
  font-family: monospace;
  font-weight: 700;
  color: #2563eb;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.tcl-route-card.route-exp .tcl-route-num { color: #d97706; }
.tcl-route-card.route-vlsi .tcl-route-num { color: #0891b2; }
.tcl-route-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 10px 0 10px;
  color: var(--tcl-heading);
}
.tcl-route-desc {
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--md-default-fg-color--light);
  margin-bottom: 18px;
}

/* Feature Pillars Grid */
.tcl-pillars {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
  margin: 20px 0 36px;
}
.tcl-pillar-card {
  padding: 24px;
  border-radius: 12px;
  border: 1px solid var(--tcl-border);
  background: var(--tcl-surface);
  transition: all 0.2s ease;
}
.tcl-pillar-card:hover {
  border-color: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.05);
}
.tcl-pillar-icon {
  font-size: 1.8rem;
  margin-bottom: 10px;
}
.tcl-pillar-title {
  font-size: 1.05rem;
  font-weight: 700;
  margin: 4px 0 8px;
  color: var(--tcl-heading);
}
.tcl-pillar-desc {
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--md-default-fg-color--light);
}

/* High Contrast Tables */
.md-typeset table:not([class]) {
  border: 1px solid var(--tcl-border) !important;
  border-radius: 8px !important;
  overflow: hidden !important;
}
.md-typeset table:not([class]) th {
  background: var(--tcl-surface) !important;
  color: var(--tcl-heading) !important;
  font-weight: 700 !important;
  border-bottom: 2px solid var(--tcl-border) !important;
}
.md-typeset table:not([class]) td {
  border-bottom: 1px solid var(--tcl-border) !important;
}
"""
    (css_dir / "extra.css").write_text(css_content, encoding="utf-8")


def write_home_pages(meta: list[tuple[int, str, str]]) -> None:
    en_rows = []
    zh_rows = []
    ms_rows = []
    fr_rows = []
    for w, en_short, zh_short in meta:
        en_rows.append(f"| Lesson {w:02d} | [{en_short}](lessons/week{w}/index.md) | [Examples](lessons/week{w}/examples.md) |")
        zh_rows.append(f"| 第 {w:02d} 课 | [{zh_short}](lessons/week{w}/index.md) | [示例代码](lessons/week{w}/examples.md) |")
        ms_rows.append(f"| Pelajaran {w:02d} | [{en_short}](lessons/week{w}/index.md) | [Contoh Kod](lessons/week{w}/examples.md) |")
        fr_rows.append(f"| Leçon {w:02d} | [{en_short}](lessons/week{w}/index.md) | [Exemples de Code](lessons/week{w}/examples.md) |")

    en_index = f"""<div class="tcl-hero">
  <div class="tcl-badge-cluster">
    <span class="tcl-badge">CC BY 4.0</span>
    <span class="tcl-badge">SJTU-YONGFU-RESEARCH-GRP</span>
    <span class="tcl-badge purple">Tcl Quiz & Practice</span>
    <span class="tcl-badge blue">Interactive WASM Lab</span>
    <span class="tcl-badge green">DRV Layout Practice</span>
    <span class="tcl-badge cyan">Multi-Language i18n</span>
  </div>

  <h1 class="tcl-hero-title">Tcl for VLSI · Beginner Scripting & DRV Practice</h1>

  <div class="tcl-hero-subtitle">
    A practical, hands-on learning lab to help beginners understand Tcl fundamentals and learn how scripting is applied in IC layout and Design Rule Violation (DRV) analysis.
  </div>

  <div class="tcl-cta-group">
    <a href="quiz/" class="tcl-btn tcl-btn-primary" style="background: linear-gradient(135deg, #4f46e5, #7c3aed); border: none;">🎯 Tcl Quiz & Cert</a>
    <a href="leaderboard/" class="tcl-btn tcl-btn-accent" style="background: linear-gradient(135deg, #059669, #0d9488); border: none;">🏆 Hall of Fame</a>
    <a href="wasm-lab/" target="_blank" class="tcl-btn tcl-btn-secondary">🚀 Launch WASM Workshop ↗</a>
    <a href="quest/" class="tcl-btn tcl-btn-secondary">🎮 Tcl Quest (RPG)</a>
    <a href="lessons/week1/" class="tcl-btn tcl-btn-secondary">📖 Lesson 1 →</a>
  </div>
</div>

<div class="tcl-fact-strip">
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">40 Lessons</span>
    <span class="tcl-fact-lbl">Curriculum Plan</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">4 Modules</span>
    <span class="tcl-fact-lbl">Tcl Quiz & Practice</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">18 Labs</span>
    <span class="tcl-fact-lbl">Hands-on Exercises</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">20 Levels</span>
    <span class="tcl-fact-lbl">Gamified RPG Quest</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">100%</span>
    <span class="tcl-fact-lbl">Browser WASM Zero-Install</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">Zero License</span>
    <span class="tcl-fact-lbl">DRV-Lite Layout Viewer</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">Beginner</span>
    <span class="tcl-fact-lbl">Hands-on DRV Practice</span>
  </div>
</div>

<div class="tcl-tools-section-title">⚡ Interactive EDA Lab Tools, Quizzes & Sandboxes</div>

<div class="tcl-tools-grid">
  <a href="quiz/" class="tcl-tool-card" style="border-left: 4px solid #6366f1;">
    <div class="tcl-tool-icon">🎯</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">Tcl Quiz Challenge</div>
      <div class="tcl-tool-desc">Test your Tcl scripting knowledge across core syntax, procedures, and data structures with a verifiable completion certificate.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="leaderboard/" class="tcl-tool-card" style="border-left: 4px solid #10b981;">
    <div class="tcl-tool-icon">🏆</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">Public Leaderboard & Hall of Fame</div>
      <div class="tcl-tool-desc">Cohort rankings, completion benchmarks, instant certificate hash verification, and performance percentiles.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="help/layout_viewer/" class="tcl-tool-card">
    <div class="tcl-tool-icon">📐</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">DRV-Lite Layout Visualizer</div>
      <div class="tcl-tool-desc">Zero-license physical design canvas with live cell placement, routing channels, and DRC violation highlighting.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="help/timing_calculator/" class="tcl-tool-card">
    <div class="tcl-tool-icon">⚡</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">STA Timing Analysis Lab</div>
      <div class="tcl-tool-desc">Beginner-friendly clock period, datapath delay, and setup slack margin calculator with visual feedback.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="exercises/" class="tcl-tool-card">
    <div class="tcl-tool-icon">📝</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">18 Practice Exercises</div>
      <div class="tcl-tool-desc">Hands-on lab problems parsing cell libraries, pin mappings, DEF files, and basic timing reports.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="capstone/" class="tcl-tool-card">
    <div class="tcl-tool-icon">🛠️</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">6 Capstone Projects</div>
      <div class="tcl-tool-desc">Practical mini-projects from routing scrapers to automated ECO wirelength fixers.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>
</div>

## 🎯 Recommended Learning Pathways

Choose the path tailored to your background and engineering goals:

<div class="tcl-routes">
  <div class="tcl-route-card">
    <span class="tcl-route-num">PATHWAY 01 · First Steps</span>
    <div class="tcl-route-title">New to Scripting</div>
    <div class="tcl-route-desc">
      Begin with <code>puts</code>, variables, and comments. Learn the 3-step substitution model (Grouping $\to$ Substitution $\to$ Invocation) to understand curly braces <code>{{}}</code> vs double quotes <code>""</code>.
    </div>
    <a href="lessons/week1/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">Start Lesson 1 →</a>
  </div>

  <div class="tcl-route-card route-exp">
    <span class="tcl-route-num">PATHWAY 02 · Fast Track</span>
    <div class="tcl-route-title">Experienced in Python / C</div>
    <div class="tcl-route-desc">
      Focus on Tcl's unique mechanisms: deferred substitution, braced <code>expr</code> rules, list/dict manipulations, namespaces, and procedures.
    </div>
    <a href="help/tcl/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">Mental Model Guide →</a>
  </div>

  <div class="tcl-route-card route-vlsi">
    <span class="tcl-route-num">PATHWAY 03 · IC Layout & DRV</span>
    <div class="tcl-route-title">Physical Design Basics</div>
    <div class="tcl-route-desc">
      Explore how Tcl interacts with IC layouts using our pure-Tcl DRV-Lite viewer. Learn how scripts inspect cell coordinates, polygons, routing channels, and identify Design Rule Violations (DRV).
    </div>
    <a href="help/layout_viewer/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">DRV Layout Viewer →</a>
  </div>
</div>

---

## 🛠️ Four Core Technological Pillars

<div class="tcl-pillars">
  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">💻</div>
    <div class="tcl-pillar-title">Client-Side WebAssembly Workshop</div>
    <div class="tcl-pillar-desc">
      Interactive browser workshop: native Tcl 8.6.6 WebAssembly engine, 18 graduated modules, memory variable inspector, and beginner projects.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🎮</div>
    <div class="tcl-pillar-title">Tcl Quest · Live Execution RPG</div>
    <div class="tcl-pillar-desc">
      A 20-level Chip Island adventure where real code execution helps beginners practice Tcl commands in an engaging, step-by-step format.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">📐</div>
    <div class="tcl-pillar-title">DRV-Lite Layout Simulator</div>
    <div class="tcl-pillar-desc">
      Zero commercial EDA licenses required. Pure-Tcl layout object model helping beginners inspect cell hierarchy, polygons, and understand DRV design rule concepts.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">⚡</div>
    <div class="tcl-pillar-title">STA Timing Analysis Lab</div>
    <div class="tcl-pillar-desc">
      Beginner-friendly timing report parser: understand setup slacks, startpoints, endpoints, and learn how Tcl scripts process EDA text outputs.
    </div>
  </div>
</div>

---

## 📚 Curriculum Directory (40 Lessons)

| Lesson | Topic | Examples |
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
make week1-01         # Run Lesson 1 first example
make week21-01        # Run Lesson 21 layout script (DRV-Lite simulation)
```
"""
    (DOCS / "index.md").write_text(en_index, encoding="utf-8")

    zh_index = f"""<div class="tcl-hero">
  <div class="tcl-badge-cluster">
    <span class="tcl-badge">CC BY 4.0</span>
    <span class="tcl-badge">SJTU-YONGFU-RESEARCH-GRP</span>
    <span class="tcl-badge purple">随堂测验与结业证书</span>
    <span class="tcl-badge blue">WASM 交互工作坊</span>
    <span class="tcl-badge green">DRV-Lite 版图实战</span>
    <span class="tcl-badge cyan">中英双语多语言</span>
  </div>

  <h1 class="tcl-hero-title">Tcl for VLSI · 从基础语法到 DRV 实战应用</h1>

  <div class="tcl-hero-subtitle">
    专为初学者打造的实用实训平台，帮助新手快速掌握 Tcl 核心语法，并理解其在芯片物理设计与 DRV（设计规则违规）版图分析中的实际应用。
  </div>

  <div class="tcl-cta-group">
    <a href="quiz/" class="tcl-btn tcl-btn-primary" style="background: linear-gradient(135deg, #4f46e5, #7c3aed); border: none;">🎯 随堂测验与证书认证</a>
    <a href="leaderboard/" class="tcl-btn tcl-btn-accent" style="background: linear-gradient(135deg, #059669, #0d9488); border: none;">🏆 荣耀榜与防伪校验</a>
    <a href="wasm-lab/" target="_blank" class="tcl-btn tcl-btn-secondary">🚀 进入 WASM 交互工作坊 ↗</a>
    <a href="quest/" class="tcl-btn tcl-btn-secondary">🎮 芯片岛 RPG 冒险</a>
    <a href="lessons/week1/" class="tcl-btn tcl-btn-secondary">📖 开始第 1 课 →</a>
  </div>
</div>

<div class="tcl-fact-strip">
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">40 课</span>
    <span class="tcl-fact-lbl">系统进阶课程</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">4 大模块</span>
    <span class="tcl-fact-lbl">随堂测验与证书</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">18 项</span>
    <span class="tcl-fact-lbl">交互实战演练</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">20 关</span>
    <span class="tcl-fact-lbl">芯片岛代码闯关</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">100%</span>
    <span class="tcl-fact-lbl">浏览器 WASM 零安装</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">零授权</span>
    <span class="tcl-fact-lbl">DRV-Lite 版图可视化</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">零基础</span>
    <span class="tcl-fact-lbl">DRV 版图实训入门</span>
  </div>
</div>

<div class="tcl-tools-section-title">⚡ 交互式实验工具、随堂测验与实战演练</div>

<div class="tcl-tools-grid">
  <a href="quiz/" class="tcl-tool-card" style="border-left: 4px solid #6366f1;">
    <div class="tcl-tool-icon">🎯</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">Tcl 随堂测验挑战</div>
      <div class="tcl-tool-desc">检验 Tcl 核心语法、过程封装与数据结构掌握情况，错题加时强化，并可获得专属防伪结课证书。</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="leaderboard/" class="tcl-tool-card" style="border-left: 4px solid #10b981;">
    <div class="tcl-tool-icon">🏆</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">公开荣耀榜与证书校验</div>
      <div class="tcl-tool-desc">全域排行榜、完成度基准、证书防伪哈希实时核验与多维度能力诊断雷达。</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="help/layout_viewer/" class="tcl-tool-card">
    <div class="tcl-tool-icon">📐</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">DRV-Lite 版图仿真可视化</div>
      <div class="tcl-tool-desc">免商业授权版图仿真画布，支持标准单元摆放、走线通道与 DRC 间距违规实时高亮。</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="help/timing_calculator/" class="tcl-tool-card">
    <div class="tcl-tool-icon">⚡</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">STA 时序分析入门计算器</div>
      <div class="tcl-tool-desc">直观调节时钟周期、数据路径与时序裕量（Slack），掌握 EDA 文本报表与裕量分析的基本概念。</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="exercises/" class="tcl-tool-card">
    <div class="tcl-tool-icon">📝</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">18 项实战演练习题</div>
      <div class="tcl-tool-desc">解析标准单元库、引脚映射、DEF 物理版图与真实 STA 时序报告的阶梯式实战任务。</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="capstone/" class="tcl-tool-card">
    <div class="tcl-tool-icon">🛠️</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">6 大综合实践项目</div>
      <div class="tcl-tool-desc">从自动走线抓取、DRV 违规收敛到自动化 ECO 线长修复的实战项目。</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>
</div>

## 🎯 你的学习起点：三种推荐路线

根据你的专业背景与编程经验，选择最契合的学习路径：

<div class="tcl-routes">
  <div class="tcl-route-card">
    <span class="tcl-route-num">PATHWAY 01 · 零基础启航</span>
    <div class="tcl-route-title">第一次学习编程</div>
    <div class="tcl-route-desc">
      从 <code>puts</code>、变量与注释入门。通过三步置换模型（切分 $\to$ 置换 $\to$ 调用），彻底理解大括号 <code>{{}}</code> 与双引号 <code>""</code> 的本质差异，告别初学者易犯的语法迷茫。
    </div>
    <a href="lessons/week1/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">从第 1 课开始 →</a>
  </div>

  <div class="tcl-route-card route-exp">
    <span class="tcl-route-num">PATHWAY 02 · 快速转栈</span>
    <div class="tcl-route-title">已有 Python / C 经验</div>
    <div class="tcl-route-desc">
      聚焦 Tcl 独特机制：大括号延迟求值、<code>expr</code> 严格花括号保护（防注入与字节编译加速）、列表与字典高效操纵、命名空间与过程封装。
    </div>
    <a href="help/tcl/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">置换心智指南 →</a>
  </div>

  <div class="tcl-route-card route-vlsi">
    <span class="tcl-route-num">PATHWAY 03 · 版图与 DRV</span>
    <div class="tcl-route-title">物理设计初学者</div>
    <div class="tcl-route-desc">
      无需商业 EDA 许可证，直接在标准 <code>tclsh</code> 下体验纯 Tcl DRV-Lite 版图操作。了解脚本如何读取单元坐标与多边形，以及如何用于识别和分析设计规则违规（DRV）。
    </div>
    <a href="help/layout_viewer/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">DRV 版图可视化 →</a>
  </div>
</div>

---

## 🛠️ 四大核心技术支柱

<div class="tcl-pillars">
  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">💻</div>
    <div class="tcl-pillar-title">纯客户端 WebAssembly 交互工作坊</div>
    <div class="tcl-pillar-desc">
      集成原生 Tcl 8.6.6 WebAssembly 运行时、18 项渐进实战、内存变量观察台与初学者实战练习。
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🎮</div>
    <div class="tcl-pillar-title">Tcl Quest · 真实代码驱动 RPG 冒险</div>
    <div class="tcl-pillar-desc">
      20 关芯片岛交互闯关，代码执行直接驱动角色走动与剧情演出，降低新手上手认知门槛。
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">📐</div>
    <div class="tcl-pillar-title">DRV-Lite 纯 Tcl 版图轻量仿真</div>
    <div class="tcl-pillar-desc">
      无需商业许可证即可入门。纯 Tcl 实现的 <code>layout</code> 对象结构，帮助初学者直观理解单元层级、多边形坐标以及 DRV 设计规则违规的基本原理。
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">⚡</div>
    <div class="tcl-pillar-title">STA 时序分析入门实验</div>
    <div class="tcl-pillar-desc">
      面向初学者的时序文本解析练习，理解时序裕量（Slack）计算，掌握 Tcl 处理 EDA 报表的基本方法。
    </div>
  </div>
</div>

---

## 📚 课程目录 (40 课)

| 课次 | 主题 | 示例代码 |
| :---: | :--- | :---: |
{chr(10).join(zh_rows)}

---

## 🚀 快速上手 (CLI)

```bash
git clone {GITHUB}.git
cd tcl-language

make check-env        # 检查本地环境与 DRV-Lite 状态
make drvlite-test     # 运行 DRV-Lite 版图仿真器 6 项单元自测
make timing-demo      # 运行 STA 静态时序分析入门实验
make week1-01         # 运行第 1 课范例脚本
make week21-01        # 运行第 21 课版图脚本 (DRV-Lite 仿真)
```
"""
    (DOCS / "index.zh.md").write_text(zh_index, encoding="utf-8")

    ms_index = f"""<div class="tcl-hero">
  <div class="tcl-badge-cluster">
    <span class="tcl-badge">CC BY 4.0</span>
    <span class="tcl-badge">SJTU-YONGFU-RESEARCH-GRP</span>
    <span class="tcl-badge purple">Kuiz Tcl & Latihan</span>
    <span class="tcl-badge blue">Bengkel Interaktif WASM</span>
    <span class="tcl-badge green">Amalan Susun Atur DRV</span>
    <span class="tcl-badge cyan">Sokongan Pelbagai Bahasa</span>
  </div>

  <h1 class="tcl-hero-title">Tcl untuk VLSI · Daripada Sintaks Asas hingga Penskripan DRV</h1>

  <div class="tcl-hero-subtitle">
    Platform pembelajaran praktikal untuk membantu pemula memahami asas penskripan Tcl dan bagaimana ia diaplikasikan dalam reka bentuk fizikal IC serta analisis susun atur DRV (Design Rule Violation).
  </div>

  <div class="tcl-cta-group">
    <a href="quiz/" class="tcl-btn tcl-btn-primary" style="background: linear-gradient(135deg, #4f46e5, #7c3aed); border: none;">🎯 Kuiz Tcl & Sijil</a>
    <a href="leaderboard/" class="tcl-btn tcl-btn-accent" style="background: linear-gradient(135deg, #059669, #0d9488); border: none;">🏆 Papan Juara & Pengesahan</a>
    <a href="wasm-lab/" target="_blank" class="tcl-btn tcl-btn-secondary">🚀 Lancarkan Bengkel WASM ↗</a>
    <a href="quest/" class="tcl-btn tcl-btn-secondary">🎮 Tcl Quest (Pulau Cip)</a>
    <a href="lessons/week1/" class="tcl-btn tcl-btn-secondary">📖 Mula Pelajaran 1 →</a>
  </div>
</div>

<div class="tcl-fact-strip">
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">40 Pelajaran</span>
    <span class="tcl-fact-lbl">Pelan Kurikulum</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">4 Modul</span>
    <span class="tcl-fact-lbl">Kuiz Tcl & Sijil</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">18 Makmal</span>
    <span class="tcl-fact-lbl">Latihan Amali Praktikal</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">20 Tahap</span>
    <span class="tcl-fact-lbl">Pengembaraan RPG</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">100%</span>
    <span class="tcl-fact-lbl">WASM Sifar Pemasangan</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">Sifar Lesen</span>
    <span class="tcl-fact-lbl">Simulator Susun Atur DRV-Lite</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">Pemula</span>
    <span class="tcl-fact-lbl">Amalan Susun Atur DRV</span>
  </div>
</div>

<div class="tcl-tools-section-title">⚡ Makmal & Alat EDA Interaktif, Kuiz & Kotak Pasir</div>

<div class="tcl-tools-grid">
  <a href="quiz/" class="tcl-tool-card" style="border-left: 4px solid #6366f1;">
    <div class="tcl-tool-icon">🎯</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">Cabaran Kuiz Tcl</div>
      <div class="tcl-tool-desc">Uji pengetahuan penskripan Tcl anda merangkumi sintaks teras, prosedur, dan struktur data dengan sijil pengesahan digital.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="leaderboard/" class="tcl-tool-card" style="border-left: 4px solid #10b981;">
    <div class="tcl-tool-icon">🏆</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">Papan Juara Awam & Sijil</div>
      <div class="tcl-tool-desc">Penanda aras pencapaian secara langsung, pengesah cincangan sijil, dan analisis kemajuan pembelajaran.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="help/layout_viewer/" class="tcl-tool-card">
    <div class="tcl-tool-icon">📐</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">Visualiser Susun Atur DRV-Lite</div>
      <div class="tcl-tool-desc">Kanvas reka bentuk fizikal sifar lesen dengan peletakan sel, saluran penghalaan, dan penonjolan pelanggaran DRC secara langsung.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="help/timing_calculator/" class="tcl-tool-card">
    <div class="tcl-tool-icon">⚡</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">Makmal Analisis Pemasaan STA</div>
      <div class="tcl-tool-desc">Tolok margin persediaan masa interaktif, tempoh jam, kelewatan laluan data dengan visualisasi mudah difahami.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="exercises/" class="tcl-tool-card">
    <div class="tcl-tool-icon">📝</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">18 Latihan Amali</div>
      <div class="tcl-tool-desc">Latihan makmal praktikal menghurai perpustakaan sel, pemetaan pin, fail DEF, dan laporan pemasaan asas.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="capstone/" class="tcl-tool-card">
    <div class="tcl-tool-icon">🛠️</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">6 Projek Capstone Praktikal</div>
      <div class="tcl-tool-desc">Projek mini praktikal daripada pengikis penghalaan hingga pembaikan panjang wayar ECO automatik.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>
</div>

## 🎯 Laluan Pembelajaran Disyorkan

Pilih laluan pembelajaran yang disesuaikan dengan latar belakang dan matlamat kejuruteraan anda:

<div class="tcl-routes">
  <div class="tcl-route-card">
    <span class="tcl-route-num">LALUAN 01 · Langkah Pertama</span>
    <div class="tcl-route-title">Baharu dalam Pengaturcaraan</div>
    <div class="tcl-route-desc">
      Bermula dengan <code>puts</code>, pembolehubah, dan ulasan kod. Kuasai model penilaian 3-langkah (Kumpulan $\to$ Penggantian $\to$ Seruan) untuk memahami perbezaan antara kurungan kerinting <code>{{}}</code> dan tanda petikan ganda <code>""</code>.
    </div>
    <a href="lessons/week1/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">Mula Pelajaran 1 →</a>
  </div>

  <div class="tcl-route-card route-exp">
    <span class="tcl-route-num">LALUAN 02 · Laluan Pantas</span>
    <div class="tcl-route-title">Berpengalaman dalam Python / C</div>
    <div class="tcl-route-desc">
      Fokus pada mekanisme unik Tcl: penilaian tertunda, peraturan <code>expr</code> berkurung, manipulasi senarai/kamus, ruang nama, dan prosedur.
    </div>
    <a href="help/tcl/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">Panduan Model Mental →</a>
  </div>

  <div class="tcl-route-card route-vlsi">
    <span class="tcl-route-num">LALUAN 03 · Susun Atur & DRV</span>
    <div class="tcl-route-title">Asas Reka Bentuk Fizikal</div>
    <div class="tcl-route-desc">
      Terokai bagaimana Tcl berinteraksi dengan susun atur IC menggunakan penonton DRV-Lite tulin Tcl kami. Pelajari bagaimana skrip memeriksa koordinat sel, poligon, dan mengenalpasti pelanggaran peraturan reka bentuk (DRV).
    </div>
    <a href="help/layout_viewer/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">Penonton Susun Atur DRV →</a>
  </div>
</div>

---

## 🛠️ Empat Tonggak Teknologi Utama

<div class="tcl-pillars">
  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">💻</div>
    <div class="tcl-pillar-title">Bengkel WebAssembly Sisi Pelanggan</div>
    <div class="tcl-pillar-desc">
      Bengkel interaktif pelayar: enjin Tcl 8.6.6 WebAssembly asli, 18 modul berperingkat, pemantau pembolehubah memori, dan latihan permulaan.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🎮</div>
    <div class="tcl-pillar-title">Tcl Quest · RPG Pacuan Kod Sebenar</div>
    <div class="tcl-pillar-desc">
      Pengembaraan 20 tahap di Pulau Cip di mana pelaksanaan kod sebenar memacu jalan cerita dan animasi secara interaktif.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">📐</div>
    <div class="tcl-pillar-title">Simulator Susun Atur DRV-Lite</div>
    <div class="tcl-pillar-desc">
      Sifar lesen komersial diperlukan. Model objek tulin Tcl untuk membantu pemula memahami hierarki sel, poligon, dan konsep peraturan reka bentuk DRV.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">⚡</div>
    <div class="tcl-pillar-title">Makmal Analisis Pemasaan STA</div>
    <div class="tcl-pillar-desc">
      Penghurai laporan pemasaan mesra pemula: memahami slack persediaan dan mempelajari cara skrip Tcl memproses output teks EDA.
    </div>
  </div>
</div>

---

## 📚 Direktori Kurikulum (40 Pelajaran)

| Pelajaran | Topik | Contoh Kod |
| :---: | :--- | :---: |
{chr(10).join(ms_rows)}

---

## 🚀 Mula Pantas (CLI)

```bash
git clone {GITHUB}.git
cd tcl-language

make check-env        # Sahkan tclsh & simulator susun atur DRV-Lite
make drvlite-test     # Jalankan 6 ujian unit pada simulator DRV-Lite
make timing-demo      # Jalankan makmal analisis pemasaan STA
make week1-01         # Jalankan contoh pertama Pelajaran 1
make week21-01        # Jalankan skrip susun atur Pelajaran 21 (simulasi DRV-Lite)
```
"""
    (DOCS / "index.ms.md").write_text(ms_index, encoding="utf-8")

    fr_index = f"""<div class="tcl-hero">
  <div class="tcl-badge-cluster">
    <span class="tcl-badge">CC BY 4.0</span>
    <span class="tcl-badge">SJTU-YONGFU-RESEARCH-GRP</span>
    <span class="tcl-badge purple">Quiz Tcl & Pratique</span>
    <span class="tcl-badge blue">Atelier Interactif WASM</span>
    <span class="tcl-badge green">Pratique de Layout DRV</span>
    <span class="tcl-badge cyan">Support Multilingue i18n</span>
  </div>

  <h1 class="tcl-hero-title">Tcl pour VLSI · De la Syntaxe de Base à la Pratique DRV</h1>

  <div class="tcl-hero-subtitle">
    Une plateforme d'apprentissage pratique conçue pour aider les débutants à comprendre les bases du script Tcl et son utilisation concrète dans l'analyse de layout et les violations de règles de conception (DRV).
  </div>

  <div class="tcl-cta-group">
    <a href="quiz/" class="tcl-btn tcl-btn-primary" style="background: linear-gradient(135deg, #4f46e5, #7c3aed); border: none;">🎯 Quiz Tcl & Certificat</a>
    <a href="leaderboard/" class="tcl-btn tcl-btn-accent" style="background: linear-gradient(135deg, #059669, #0d9488); border: none;">🏆 Tableau des Scores & Vérification</a>
    <a href="wasm-lab/" target="_blank" class="tcl-btn tcl-btn-secondary">🚀 Lancer l'Atelier WASM ↗</a>
    <a href="quest/" class="tcl-btn tcl-btn-secondary">🎮 Tcl Quest (Île RPG)</a>
    <a href="lessons/week1/" class="tcl-btn tcl-btn-secondary">📖 Démarrer Leçon 1 →</a>
  </div>
</div>

<div class="tcl-fact-strip">
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">40 Leçons</span>
    <span class="tcl-fact-lbl">Programme Complet</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">4 Modules</span>
    <span class="tcl-fact-lbl">Quiz Tcl & Certificat</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">18 Labos</span>
    <span class="tcl-fact-lbl">Exercices Pratiques</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">20 Niveaux</span>
    <span class="tcl-fact-lbl">Quête RPG Interactive</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">100%</span>
    <span class="tcl-fact-lbl">Zéro Installation Navigateur WASM</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">Zéro Licence</span>
    <span class="tcl-fact-lbl">Simulateur de Layout DRV-Lite</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">Débutant</span>
    <span class="tcl-fact-lbl">Pratique de Layout DRV</span>
  </div>
</div>

<div class="tcl-tools-section-title">⚡ Outils & Laboratoires Interactifs EDA, Quiz & Bacs à Sable</div>

<div class="tcl-tools-grid">
  <a href="quiz/" class="tcl-tool-card" style="border-left: 4px solid #6366f1;">
    <div class="tcl-tool-icon">🎯</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">Défi Quiz Tcl</div>
      <div class="tcl-tool-desc">Testez vos connaissances en script Tcl sur la syntaxe de base, les procédures et les structures de données avec un certificat numérique vérifiable.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="leaderboard/" class="tcl-tool-card" style="border-left: 4px solid #10b981;">
    <div class="tcl-tool-icon">🏆</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">Tableau d'Honneur Public & Certificats</div>
      <div class="tcl-tool-desc">Classement en direct de la cohorte, vérificateur de certificat par empreinte cryptographique et bilan diagnostique complet.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="help/layout_viewer/" class="tcl-tool-card">
    <div class="tcl-tool-icon">📐</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">Visualiseur de Layout DRV-Lite</div>
      <div class="tcl-tool-desc">Canevas de conception physique sans licence commerciale avec placement de cellules, canaux de routage et détection des violations DRC.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="help/timing_calculator/" class="tcl-tool-card">
    <div class="tcl-tool-icon">⚡</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">Labo d'Analyse Temporelle STA</div>
      <div class="tcl-tool-desc">Calculateur interactif de marge temporelle, période d'horloge et délai de trajet pour comprendre les concepts de base du timing EDA.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="exercises/" class="tcl-tool-card">
    <div class="tcl-tool-icon">📝</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">18 Exercices Pratiques</div>
      <div class="tcl-tool-desc">Problèmes de laboratoire analysant des bibliothèques de cellules, correspondances de broches, fichiers DEF et rapports temporels de base.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>

  <a href="capstone/" class="tcl-tool-card">
    <div class="tcl-tool-icon">🛠️</div>
    <div class="tcl-tool-body">
      <div class="tcl-tool-title">6 Projets Capstone Pratiques</div>
      <div class="tcl-tool-desc">Mini-projets pratiques, de l'extraction de routage à la correction automatique de longueur de fil ECO.</div>
    </div>
    <div class="tcl-tool-arrow">→</div>
  </a>
</div>

## 🎯 Parcours d'Apprentissage Recommandés

Choisissez le parcours adapté à votre profil et à vos objectifs d'ingénierie :

<div class="tcl-routes">
  <div class="tcl-route-card">
    <span class="tcl-route-num">PARCOURS 01 · Premiers Pas</span>
    <div class="tcl-route-title">Débutant en Programmation</div>
    <div class="tcl-route-desc">
      Commencez par <code>puts</code>, les variables et les commentaires. Maîtrisez le modèle en 3 étapes (Regroupement $\to$ Substitution $\to$ Évaluation) pour comprendre les accolades <code>{{}}</code> par rapport aux guillemets <code>""</code>.
    </div>
    <a href="lessons/week1/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">Démarrer Leçon 1 →</a>
  </div>

  <div class="tcl-route-card route-exp">
    <span class="tcl-route-num">PARCOURS 02 · Voie Rapide</span>
    <div class="tcl-route-title">Expérience en Python / C</div>
    <div class="tcl-route-desc">
      Concentrez-vous sur les spécificités de Tcl : substitution différée, règles d'<code>expr</code> entre accolades, manipulation de listes/dictionnaires, espaces de noms et procédures.
    </div>
    <a href="help/tcl/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">Guide du Modèle Mental →</a>
  </div>

  <div class="tcl-route-card route-vlsi">
    <span class="tcl-route-num">PARCOURS 03 · Layout & DRV</span>
    <div class="tcl-route-title">Bases de la Conception Physique</div>
    <div class="tcl-route-desc">
      Découvrez comment Tcl interagit avec les layouts de circuits intégrés grâce à notre visualiseur DRV-Lite en pur Tcl. Apprenez comment les scripts inspectent les cellules, polygones et violations de règles de conception (DRV).
    </div>
    <a href="help/layout_viewer/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">Visualiseur de Layout DRV →</a>
  </div>
</div>

---

## 🛠️ Quatre Piliers Technologiques Majeurs

<div class="tcl-pillars">
  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">💻</div>
    <div class="tcl-pillar-title">Atelier Client Pur WebAssembly</div>
    <div class="tcl-pillar-desc">
      Atelier interactif dans le navigateur : moteur WebAssembly Tcl 8.6.6 natif, 18 modules progressifs, inspecteur de variables mémoire et exercices pratiques.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">🎮</div>
    <div class="tcl-pillar-title">Tcl Quest · RPG Piloté par le Code</div>
    <div class="tcl-pillar-desc">
      Aventure de 20 niveaux sur l'Île des Puces où l'exécution du code réel pilote les cinématiques de manière engageante pour les débutants.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">📐</div>
    <div class="tcl-pillar-title">Simulateur de Layout DRV-Lite</div>
    <div class="tcl-pillar-desc">
      Aucune licence commerciale requise. Modèle d'objets en pur Tcl aidant les débutants à comprendre la hiérarchie de cellules, les polygones et les règles DRV.
    </div>
  </div>

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">⚡</div>
    <div class="tcl-pillar-title">Labo d'Analyse Temporelle STA</div>
    <div class="tcl-pillar-desc">
      Analyseur de rapports temporels pour débutants : comprenez la marge temporelle (slack) et découvrez comment les scripts Tcl traitent les rapports EDA.
    </div>
  </div>
</div>

---

## 📚 Programme d'Études (40 Leçons)

| Leçon | Sujet | Exemples de Code |
| :---: | :--- | :---: |
{chr(10).join(fr_rows)}

---

## 🚀 Démarrage Rapide (CLI)

```bash
git clone {GITHUB}.git
cd tcl-language

make check-env        # Vérifier tclsh & le simulateur DRV-Lite
make drvlite-test     # Lancer 6 tests unitaires sur le simulateur DRV-Lite
make timing-demo      # Lancer le labo de temporisation STA
make week1-01         # Exécuter le premier exemple de la Leçon 1
make week21-01        # Exécuter le script de layout de la Leçon 21 (DRV-Lite)
```
"""
    (DOCS / "index.fr.md").write_text(fr_index, encoding="utf-8")


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
        en_body = re.sub(r"^#\s*Week\s+(\d+)", r"# Lesson \1", en_body, flags=re.MULTILINE)
        zh_body = re.sub(r"^#\s*第\s*(\d+)\s*周", r"# 第 \1 课", zh_body, flags=re.MULTILINE)

        (out_dir / "index.md").write_text(en_body, encoding="utf-8")
        (out_dir / "index.zh.md").write_text(zh_body, encoding="utf-8")
        (out_dir / "examples.md").write_text(examples_page(wdir, week, "en"), encoding="utf-8")
        (out_dir / "examples.zh.md").write_text(examples_page(wdir, week, "zh"), encoding="utf-8")

        meta.append((week, en_short, zh_short))
    return meta


def write_mkdocs_yml(meta: list[tuple[int, str, str]]) -> None:
    m10_nav, m20_nav, m30_nav, m40_nav = [], [], [], []
    nav_trans_weeks = []
    ms_nav_trans_weeks = []
    fr_nav_trans_weeks = []

    m_titles = [
        ("M10: Tcl Core Syntax (Lessons 01–10)", "M10: Tcl 核心语法 (第 01–10 课)"),
        ("M20: Fluency & OOP (Lessons 11–20)", "M20: 流畅编程与面向对象 (第 11–20 课)"),
        ("M30: Calibre Layout Core (Lessons 21–30)", "M30: Calibre 版图核心 (第 21–30 课)"),
        ("M40: Layout Catalog & Sign-Off (Lessons 31–40)", "M40: 版图全家桶与审计 (第 31–40 课)"),
    ]
    for en_m, zh_m in m_titles:
        nav_trans_weeks.append(f'            "{en_m}": "{zh_m}"')

    ms_m_titles = [
        ("M10: Tcl Core Syntax (Lessons 01–10)", "M10: Sintaks Teras Tcl (Pelajaran 01–10)"),
        ("M20: Fluency & OOP (Lessons 11–20)", "M20: Pengaturcaraan Lancar & OOP (Pelajaran 11–20)"),
        ("M30: Calibre Layout Core (Lessons 21–30)", "M30: Teras Susun Atur Calibre (Pelajaran 21–30)"),
        ("M40: Layout Catalog & Sign-Off (Lessons 31–40)", "M40: Katalog Susun Atur & Sign-Off (Pelajaran 31–40)"),
    ]
    for en_m, ms_m in ms_m_titles:
        ms_nav_trans_weeks.append(f'            "{en_m}": "{ms_m}"')

    fr_m_titles = [
        ("M10: Tcl Core Syntax (Lessons 01–10)", "M10: Syntaxe de Base Tcl (Leçons 01–10)"),
        ("M20: Fluency & OOP (Lessons 11–20)", "M20: Fluidité & POO (Leçons 11–20)"),
        ("M30: Calibre Layout Core (Lessons 21–30)", "M30: Cœur de Layout Calibre (Leçons 21–30)"),
        ("M40: Layout Catalog & Sign-Off (Lessons 31–40)", "M40: Catalogue Layout & Validation (Leçons 31–40)"),
    ]
    for en_m, fr_m in fr_m_titles:
        fr_nav_trans_weeks.append(f'            "{en_m}": "{fr_m}"')

    for w, en_title, zh_title in meta:
        item = (
            f'          - "Lesson {w:02d}: {en_title}":\n'
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
        nav_trans_weeks.append(f'            "Lesson {w:02d}: {en_title}": "第 {w:02d} 课: {zh_title}"')
        ms_nav_trans_weeks.append(f'            "Lesson {w:02d}: {en_title}": "Pelajaran {w:02d}: {en_title}"')
        fr_nav_trans_weeks.append(f'            "Lesson {w:02d}: {en_title}": "Leçon {w:02d}: {en_title}"')

    m10_yaml = "\n".join(m10_nav)
    m20_yaml = "\n".join(m20_nav)
    m30_yaml = "\n".join(m30_nav)
    m40_yaml = "\n".join(m40_nav)
    weeks_trans_yaml = "\n".join(nav_trans_weeks)
    ms_weeks_trans_yaml = "\n".join(ms_nav_trans_weeks)
    fr_weeks_trans_yaml = "\n".join(fr_nav_trans_weeks)

    yml = f"""# Generated by scripts/build_website.py — modern high-readability architecture
site_name: Tcl for VLSI Automation Lab
site_description: Beginner Tcl scripting lessons, DRV layout practice & interactive WASM workshop
site_url: https://sjtu-yongfu-research-grp.github.io/tcl-language/
repo_url: {GITHUB}
repo_name: tcl-language
edit_uri: ""

theme:
  name: material
  language: en
  palette:
    - scheme: default
      primary: indigo
      accent: blue
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: cyan
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode
  font:
    text: Inter
    code: JetBrains Mono
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
    - name: Bahasa Melayu
      link: /ms/
      lang: ms
    - name: Français
      link: /fr/
      lang: fr

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
          site_name: Tcl 芯片自动化与 DRV 入门实验室
          site_description: 中英双语 Tcl 入门教程与 DRV 版图自动化交互实训平台
          nav_translations:
            Home: 首页
            Quiz Challenge & Leaderboard: 测评挑战与排行榜
            Quiz Challenge & Certification: 随堂测评挑战与认证
            Public Leaderboard & Certificate: 荣誉排行榜与认证证书
            Interactive Labs & Tools: 交互实验室与实战工具
            Interactive Workshop (WASM): 交互工作坊 (WASM)
            Tcl Quest (Chip Island RPG): 芯片岛闯关冒险 (RPG)
            Web Playground: 演练台 (Playground)
            VLSI Layout Visualizer: VLSI 版图仿真可视化 (DRV-Lite)
            STA Timing Gatekeeper: STA 时序门禁计算器
            Practice & Projects: 实战与项目
            18 Practical Exercises: 18 项实战练习
            6 Capstone Data Projects: 6 大综合项目
            Homework Assignments: 课后作业
            Chapter Quizzes: 随堂自测
            Lessons (40 Lessons): 课程体系 (40 课)
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
        - locale: ms
          name: Bahasa Melayu
          build: true
          site_name: Makmal Penskripan Tcl & DRV VLSI
          site_description: Panduan Asas Penskripan Tcl, Analisis Susun Atur DRV & Bengkel Interaktif WASM
          nav_translations:
            Home: Laman Utama
            Quiz Challenge & Leaderboard: Cabaran Kuiz & Papan Juara
            Quiz Challenge & Certification: Cabaran Kuiz & Pensijilan
            Public Leaderboard & Certificate: Papan Pendahulu & Pensijilan
            Interactive Labs & Tools: Makmal & Alat Interaktif
            Interactive Workshop (WASM): Bengkel Interaktif (WASM)
            Tcl Quest (Chip Island RPG): Tcl Quest (Pengembaraan Pulau Cip)
            Web Playground: Taman Permainan Kod (Playground)
            VLSI Layout Visualizer: Visualiser Susun Atur VLSI (DRV-Lite)
            STA Timing Gatekeeper: Penjaga Masa STA (Slack & WNS/TNS)
            Practice & Projects: Latihan & Projek
            18 Practical Exercises: 18 Latihan Amali
            6 Capstone Data Projects: 6 Projek Capstone Data
            Homework Assignments: Tugasan Kerja Rumah
            Chapter Quizzes: Kuiz Bab
            Lessons (40 Lessons): Sukatan Pelajaran (40 Pelajaran)
            EDA Tools & Guides: Alat EDA & Panduan
            DRV-Lite Layout Simulator: Simulator Susun Atur DRV-Lite
            STA Timing Analysis Lab: Makmal Analisis Masa STA
            Tcl Mental Model Guide: Panduan Model Mental Tcl
            Calibre Command Reference: Rujukan Perintah Calibre
            Knowledge Graph Coverage: Liputan Graf Pengetahuan
            Contributors: Penyumbang & Penghargaan
            Lesson: Pelajaran
            Examples: Contoh Kod
{ms_weeks_trans_yaml}
        - locale: fr
          name: Français
          build: true
          site_name: Laboratoire Tcl & DRV pour VLSI
          site_description: Initiation au Script Tcl, Analyse de Layout DRV & Atelier Interactif WASM
          nav_translations:
            Home: Accueil
            Quiz Challenge & Leaderboard: Défi Quiz & Classement
            Quiz Challenge & Certification: Défi Quiz & Certification
            Public Leaderboard & Certificate: Tableau des Scores & Certification
            Interactive Labs & Tools: Labos & Outils Interactifs
            Interactive Workshop (WASM): Atelier Interactif (WASM)
            Tcl Quest (Chip Island RPG): Tcl Quest (Aventure sur l'Île des Puces)
            Web Playground: Bac à Sable Web (Playground)
            VLSI Layout Visualizer: Visualiseur de Layout VLSI (DRV-Lite)
            STA Timing Gatekeeper: Contrôleur Temporel STA (Slack & WNS/TNS)
            Practice & Projects: Pratique & Projets
            18 Practical Exercises: 18 Exercices Pratiques
            6 Capstone Data Projects: 6 Projets Capstone de Données
            Homework Assignments: Devoirs & Exercices
            Chapter Quizzes: Quiz de Chapitre
            Lessons (40 Lessons): Programme (40 Leçons)
            EDA Tools & Guides: Outils EDA & Guides
            DRV-Lite Layout Simulator: Simulateur de Layout DRV-Lite
            STA Timing Analysis Lab: Labo d'Analyse Temporelle STA
            Tcl Mental Model Guide: Guide du Modèle Mental Tcl
            Calibre Command Reference: Référence des Commandes Calibre
            Knowledge Graph Coverage: Couverture du Graphe de Connaissances
            Contributors: Contributeurs & Attribution
            Lesson: Leçon
            Examples: Exemples de Code
{fr_weeks_trans_yaml}

validation:
  omitted_files: warn
  absolute_links: info
  unrecognized_links: warn

nav:
  - Home: index.md
  - Quiz Challenge & Leaderboard:
      - Quiz Challenge & Certification: quiz.md
      - Public Leaderboard & Certificate: leaderboard.md
  - Interactive Labs & Tools:
      - Interactive Workshop (WASM): workshop.md
      - Tcl Quest (Chip Island RPG): quest.md
      - Web Playground: playground.md
      - VLSI Layout Visualizer: help/layout_viewer.md
      - STA Timing Gatekeeper: help/timing_calculator.md
  - Practice & Projects:
      - 18 Practical Exercises: exercises.md
      - 6 Capstone Data Projects: capstone.md
      - Homework Assignments: help/homework.md
      - Chapter Quizzes: help/quiz.md
  - Lessons (40 Lessons):
      - "M10: Tcl Core Syntax (Lessons 01–10)":
{m10_yaml}
      - "M20: Fluency & OOP (Lessons 11–20)":
{m20_yaml}
      - "M30: Calibre Layout Core (Lessons 21–30)":
{m30_yaml}
      - "M40: Layout Catalog & Sign-Off (Lessons 31–40)":
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
    (DOCS / "help").mkdir(parents=True, exist_ok=True)


def write_redirect_fallbacks() -> None:
    site = WEBSITE / "site"
    if not site.exists():
        return
    redirect_tmpl = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={target}">
<script>window.location.replace("{target}");</script>
<title>Redirecting...</title>
</head>
<body>
<p>Redirecting to <a href="{target}">{target}</a>...</p>
</body>
</html>
"""
    for lang in ["", "zh", "ms", "fr"]:
        base_dir = site / lang if lang else site
        quiz_dir = base_dir / "quiz"
        lb_dir = base_dir / "leaderboard"

        if quiz_dir.exists():
            (quiz_dir / "leaderboard.md").write_text(redirect_tmpl.format(target="../leaderboard/"), encoding="utf-8")
        if lb_dir.exists():
            (lb_dir / "quiz.md").write_text(redirect_tmpl.format(target="../quiz/"), encoding="utf-8")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] in ("--post-build", "--fallbacks"):
        write_redirect_fallbacks()
        print("Redirect fallbacks written successfully.")
        return

    clean_docs()
    meta = generate_weeks()
    if not meta:
        raise SystemExit("No lesson weeks found under lessons/")
    write_stylesheets()
    copy_workshop()
    copy_quest()
    copy_assets()
    write_workshop_pages()
    write_quest_pages()
    write_playground_pages()
    write_layout_viewer_pages()
    write_timing_calculator_pages()
    write_exercises_pages()
    write_capstone_pages()
    copy_help_docs()
    write_homework_pages()
    write_quiz_pages()
    write_quiz_challenge_pages(DOCS)
    write_leaderboard_pages(DOCS)
    write_contributors_pages()
    write_home_pages(meta)
    write_mkdocs_yml(meta)
    write_redirect_fallbacks()
    print(f"Generated multi-language website for {len(meta)} weeks -> {WEBSITE}")


if __name__ == "__main__":
    main()


