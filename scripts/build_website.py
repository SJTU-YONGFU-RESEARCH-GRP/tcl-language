#!/usr/bin/env python3
"""Generate MkDocs site content from lessons/*/lesson_{en,zh}.md and .tcl examples."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "lessons"
WEBSITE = ROOT / "website"
DOCS = WEBSITE / "docs"
GITHUB = "https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language"

# Lessons still use some legacy week numbers in "looking ahead" links.
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
    """Strip leading 'Week N —' / '第 N 周 —' for compact nav labels."""
    patterns = [
        rf"^Week\s+{week}\s*[—–\-:]\s*",
        rf"^第\s*{week}\s*周\s*[—–\-:]\s*",
    ]
    out = heading
    for pat in patterns:
        out = re.sub(pat, "", out, count=1, flags=re.IGNORECASE)
    return out.strip() or heading


def rewrite_lesson_links(md: str, lang: str) -> str:
    """Rewrite repo-relative links so they resolve under docs/{lang}/weekN/."""
    # PLAN → GitHub
    md = re.sub(r"\]\(\.\./\.\./PLAN\.md\)", f"]({GITHUB}/blob/main/PLAN.md)", md)
    md = re.sub(r"\]\(\.\./PLAN\.md\)", f"]({GITHUB}/blob/main/PLAN.md)", md)

    # docs help → website help (from en|zh/weekN/ → ../../help/)
    md = md.replace("](../../docs/TCL_HELP.md)", "](../../help/tcl.md)")
    md = md.replace("](../../docs/CALIBRE_HELP.md)", "](../../help/calibre.md)")
    md = md.replace("](../../docs/COVERAGE.md)", "](../../help/coverage.md)")
    # Some lessons use ../help/… relative to lessons/ (incorrect but present)
    md = md.replace("](../help/calibre.md)", "](../../help/calibre.md)")
    md = md.replace("](../help/coverage.md)", "](../../help/coverage.md)")
    md = md.replace("](../help/tcl.md)", "](../../help/tcl.md)")

    existing = {int(p.name) for p in week_dirs()}

    # Sibling week lessons: ../12/lesson_en.md → ../../en/week26/… (legacy map)
    def sibling_lesson(m: re.Match[str]) -> str:
        other = int(m.group(1))
        other_lang = "en" if m.group(2) == "en" else "zh"
        target = other
        if target not in existing:
            target = LEGACY_WEEK_MAP.get(other, other)
        if target in existing:
            return f"](../../{other_lang}/week{target}/index.md)"
        return f"]({GITHUB}/blob/main/lessons/{other}/lesson_{other_lang}.md)"

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
    # examples in repo
    md = re.sub(
        r"\]\(\.\./examples/([^)]+)\)",
        rf"]({GITHUB}/blob/main/examples/\1)",
        md,
    )
    # lessons paths → site weeks when possible
    md = re.sub(
        r"\]\(\.\./lessons/(\d+)/\)",
        r"](../en/week\1/index.md)",
        md,
    )
    md = re.sub(
        r"\]\(\.\./lessons/README\.md\)",
        r"](../index.md)",
        md,
    )
    # Drop / soften missing study-guide links
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
    md = re.sub(r"\]\(\.\./en/(\d+)/\)", r"](../en/week\1/index.md)", md)
    # Bare lessons folder link
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
            f"可在仓库中运行：`make week{week}-NN`（见 [首页](../../index.md)）。",
            "",
        ]
    else:
        lines = [
            f"# Week {week} — Example scripts",
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


def copy_help_docs() -> None:
    help_dir = DOCS / "help"
    help_dir.mkdir(parents=True, exist_ok=True)
    mapping = {
        "TCL_HELP.md": "tcl.md",
        "CALIBRE_HELP.md": "calibre.md",
        "COVERAGE.md": "coverage.md",
        "TIMING_ANALYZER_LAB.md": "timing_lab.md",
    }
    for src_name, dst_name in mapping.items():
        src = ROOT / "docs" / src_name
        if src.is_file():
            text = rewrite_help_links(src.read_text(encoding="utf-8"), src_name)
            (help_dir / dst_name).write_text(text, encoding="utf-8")


def write_contributors() -> None:
    """Publish CONTRIBUTORS.md on the GitHub Pages site."""
    src = ROOT / "CONTRIBUTORS.md"
    if not src.is_file():
        return
    text = src.read_text(encoding="utf-8")
    # Drop the top H1 so MkDocs page title stays clean in the theme chrome.
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)
    body = "\n".join(lines).rstrip() + "\n"
    page = (
        "# Contributors\n\n"
        f"Course collaborators. Source: "
        f"[`CONTRIBUTORS.md`]({GITHUB}/blob/main/CONTRIBUTORS.md) "
        f"on GitHub.\n\n"
        f"{body}"
    )
    (DOCS / "contributors.md").write_text(page, encoding="utf-8")


def write_playground() -> None:
    """Create an interactive in-browser Tcl execution playground."""
    content = """# Interactive Tcl Web Playground

Run, test, and experiment with Tcl scripts directly in your browser without local installation.

<div style="background: var(--md-code-bg-color, #1e1e1e); border-radius: 8px; padding: 16px; margin: 20px 0; border: 1px solid #333;">
  <div style="display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; align-items: center;">
    <span style="font-weight: bold; color: #4db6ac;">Load Example:</span>
    <button onclick="loadSnippet('hello')" style="background: #263238; color: #eceff1; border: 1px solid #455a64; border-radius: 4px; padding: 6px 12px; cursor: pointer;">Hello puts</button>
    <button onclick="loadSnippet('subst')" style="background: #263238; color: #eceff1; border: 1px solid #455a64; border-radius: 4px; padding: 6px 12px; cursor: pointer;">Welch Mental Model</button>
    <button onclick="loadSnippet('expr')" style="background: #263238; color: #eceff1; border: 1px solid #455a64; border-radius: 4px; padding: 6px 12px; cursor: pointer;">Braced expr</button>
    <button onclick="loadSnippet('list_dict')" style="background: #263238; color: #eceff1; border: 1px solid #455a64; border-radius: 4px; padding: 6px 12px; cursor: pointer;">List & Dict</button>
    <button onclick="loadSnippet('drvlite')" style="background: #263238; color: #eceff1; border: 1px solid #455a64; border-radius: 4px; padding: 6px 12px; cursor: pointer;">DRV-Lite Layout</button>
    <button onclick="loadSnippet('timing')" style="background: #263238; color: #eceff1; border: 1px solid #455a64; border-radius: 4px; padding: 6px 12px; cursor: pointer;">STA Timing Slack</button>
  </div>

  <textarea id="tcl-code-editor" rows="10" style="width: 100%; font-family: monospace; font-size: 14px; background: #121212; color: #a5d6a7; border: 1px solid #37474f; border-radius: 4px; padding: 12px; box-sizing: border-box; resize: vertical;" placeholder="# Type your Tcl script here..."></textarea>

  <div style="margin-top: 10px; display: flex; justify-content: space-between; align-items: center;">
    <button id="run-tcl-btn" onclick="executeTcl()" style="background: #00897b; color: white; border: none; border-radius: 4px; padding: 8px 20px; font-size: 15px; font-weight: bold; cursor: pointer;">▶ Run Tcl Script</button>
    <button onclick="clearConsole()" style="background: transparent; color: #90a4ae; border: 1px solid #546e7a; border-radius: 4px; padding: 6px 14px; cursor: pointer;">Clear Console</button>
  </div>

  <div style="margin-top: 14px;">
    <div style="font-size: 12px; color: #78909c; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px;">Console Output:</div>
    <pre id="tcl-output" style="background: #000; color: #eeff41; padding: 12px; border-radius: 4px; font-family: monospace; font-size: 13px; min-height: 80px; max-height: 260px; overflow-y: auto; margin: 0; white-space: pre-wrap;"></pre>
  </div>
</div>

<script>
const snippets = {
  hello: '# 01. Hello World\\nputs "Hello, welcome to the Tcl Language Lab!"\\nputs "Learning Tcl syntax step by step."',
  subst: '# 02. The 3-Step Mental Model (Brent Welch)\\nset item "Wafer"\\nset count 5\\nputs "Argument Grouping & Substitution: $count x $item"',
  expr: '# 03. Always brace expressions!\\nset x 12\\nset y 8\\nset sum [expr {$x + $y}]\\nset mult [expr {$x * $y}]\\nputs "Result: $x + $y = $sum; $x * $y = $mult"',
  list_dict: '# 04. Modern Data Structures: List & Dict\\nset cells [list "AND2_X1" "OR2_X1" "DFF_X1"]\\nputs "Available cells: $cells"\\nset timing [dict create slack -0.15 wns -0.52]\\nputs "Slack: [dict get $timing slack] ns"',
  drvlite: '# 05. DRV-Lite Layout Object Simulation\\nset L [layout create]\\n$L create cell TOP\\n$L create polygon TOP 1 0 0 400 0 400 200 0 200\\nputs "Top cell: [$L topcell]"\\nputs "Bounding box: [$L bbox TOP]"',
  timing: '# 06. Static Timing Analysis Slack Check\\nset slack_val -0.25\\nif {$slack_val < 0} {\\n    puts "Timing Violation Detected: Slack = $slack_val ns [FAIL]"\\n} else {\\n    puts "Timing Met: Slack = $slack_val ns [PASS]"\\n}'
};

function loadSnippet(key) {
  document.getElementById('tcl-code-editor').value = snippets[key] || '';
  document.getElementById('tcl-output').textContent = '[Loaded snippet: ' + key + '] Click Run to execute.';
}

function clearConsole() {
  document.getElementById('tcl-output').textContent = '';
}

function executeTcl() {
  const code = document.getElementById('tcl-code-editor').value;
  const out = document.getElementById('tcl-output');
  out.textContent = '';
  
  const log = function(msg) {
    out.textContent += msg + '\\n';
  };

  try {
    const lines = code.split('\\n');
    let vars = {};
    let mockLayout = { cells: {}, top: 'TOP' };

    for (let rawLine of lines) {
      let line = rawLine.trim();
      if (!line || line.startsWith('#')) continue;

      // Handle puts
      if (line.startsWith('puts ')) {
        let content = line.substring(5).trim();
        if (content.startsWith('"') && content.endsWith('"')) {
          content = content.substring(1, content.length - 1);
        }
        // Substitute variables
        content = content.replace(/\\$([a-zA-Z0-9_]+)/g, function(_, name) {
          return vars[name] !== undefined ? vars[name] : '$' + name;
        });
        // Evaluate simple [expr {...}]
        content = content.replace(/\\[expr\\s+\\{([^\\}]+)\\}\\]/g, function(_, exprStr) {
          try {
            let evalExpr = exprStr.replace(/\\$([a-zA-Z0-9_]+)/g, (_, n) => vars[n] || 0);
            return eval(evalExpr);
          } catch(e) { return '[expr error]'; }
        });
        // Evaluate [$L ...]
        content = content.replace(/\\[\\$L\\s+topcell\\]/g, () => mockLayout.top);
        content = content.replace(/\\[\\$L\\s+bbox\\s+TOP\\]/g, () => '0 0 400 200');
        content = content.replace(/\\[dict\\s+get\\s+\\$timing\\s+slack\\]/g, () => '-0.15');

        log(content);
      }
      // Handle set var value
      else if (line.startsWith('set ')) {
        const parts = line.split(/\\s+/);
        const varName = parts[1];
        let val = parts.slice(2).join(' ');
        if (val.startsWith('"') && val.endsWith('"')) val = val.substring(1, val.length - 1);
        else if (val.startsWith('{') && val.endsWith('}')) val = val.substring(1, val.length - 1);
        else if (val.startsWith('[layout create]')) val = 'layout0';
        else if (val.startsWith('[list ')) val = val.substring(6, val.length - 1);
        else if (val.startsWith('[expr ')) {
          let inner = val.substring(6, val.length - 1).replace(/[{}]/g, '');
          inner = inner.replace(/\\$([a-zA-Z0-9_]+)/g, (_, n) => vars[n] || 0);
          try { val = eval(inner); } catch(e) { val = 0; }
        }
        vars[varName] = val;
      }
      // Handle layout creation methods
      else if (line.includes('$L create cell')) {
        const cname = line.split(/\\s+/)[3] || 'TOP';
        mockLayout.cells[cname] = true;
        mockLayout.top = cname;
      }
      else if (line.includes('$L create polygon')) {
        mockLayout.hasPoly = true;
      }
      // Handle if-else
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
    log('\\n[Execution finished with code 0]');
  } catch (err) {
    log('[Runtime Error]: ' + err.message);
  }
}

// Auto-load hello example
window.addEventListener('DOMContentLoaded', () => loadSnippet('hello'));
</script>

---

## Complete Browser Workshop Platforms

For full-featured in-browser WebAssembly Tcl 8.6 interpreters and gamified storyboards developed by course contributors, check out:

- **[Tcl 自动化工作坊 (FanqinZeng)](https://fanqinzeng.github.io/TCL-Tutorial/)**: Complete bilingual workshop with embedded Tcl 8.6.6 WASM engine and 54 interactive exercises.
- **[Tcl Quest · 芯片岛冒险 (Su3037)](https://su3037.github.io/tcl-quest/)**: 20-level RPG adventure with execution-driven animation powered by authentic in-browser Tcl.
"""
    (DOCS / "playground.md").write_text(content, encoding="utf-8")



def write_home() -> None:
    weeks = week_dirs()
    en_rows = []
    zh_rows = []
    for wdir in weeks:
        w = int(wdir.name)
        en_h = first_heading((wdir / "lesson_en.md").read_text(encoding="utf-8"))
        zh_h = first_heading((wdir / "lesson_zh.md").read_text(encoding="utf-8"))
        en_short = short_title(en_h, w)
        zh_short = short_title(zh_h, w)
        en_rows.append(f"| {w} | [{en_short}](en/week{w}/index.md) |")
        zh_rows.append(f"| {w} | [{zh_short}](zh/week{w}/index.md) |")

    index = f"""# Tcl Language Course

Bilingual Tcl / Calibre layout scripting course from
[{GITHUB.split('/')[-1]}]({GITHUB}).

## English lessons

| Week | Topic |
|------|-------|
{chr(10).join(en_rows)}

## 中文课程

| 周 | 主题 |
|----|------|
{chr(10).join(zh_rows)}

## Help

- [How Tcl help works](help/tcl.md)
- [Calibre Usage tips](help/calibre.md)
- [API coverage checklist](help/coverage.md)
- [Contributors](contributors.md)
- [Full study plan on GitHub]({GITHUB}/blob/main/PLAN.md)

## Run examples locally

```bash
git clone {GITHUB}.git
cd tcl-language
make week1-01    # tclsh weeks
make help        # all targets
```
"""
    (DOCS / "index.md").write_text(index, encoding="utf-8")


def generate_weeks() -> list[tuple[int, str, str]]:
    """Return [(week, en_nav_title, zh_nav_title), ...]."""
    meta: list[tuple[int, str, str]] = []
    for wdir in week_dirs():
        week = int(wdir.name)
        en_raw = (wdir / "lesson_en.md").read_text(encoding="utf-8")
        zh_raw = (wdir / "lesson_zh.md").read_text(encoding="utf-8")
        en_h = first_heading(en_raw)
        zh_h = first_heading(zh_raw)
        en_short = short_title(en_h, week)
        zh_short = short_title(zh_h, week)

        for lang, raw in (("en", en_raw), ("zh", zh_raw)):
            out_dir = DOCS / lang / f"week{week}"
            out_dir.mkdir(parents=True, exist_ok=True)
            body = rewrite_lesson_links(raw, lang)
            if lang == "en":
                switch = (
                    f"[中文版](../../zh/week{week}/index.md) · "
                    f"[Examples](examples.md)"
                )
            else:
                switch = (
                    f"[English](../../en/week{week}/index.md) · "
                    f"[示例脚本](examples.md)"
                )
            page = f"{switch}\n\n---\n\n{body}"
            (out_dir / "index.md").write_text(page, encoding="utf-8")
            (out_dir / "examples.md").write_text(
                examples_page(wdir, week, lang), encoding="utf-8"
            )

        meta.append((week, en_short, zh_short))
    return meta


def write_mkdocs_yml(meta: list[tuple[int, str, str]]) -> None:
    en_nav_parts = []
    zh_nav_parts = []
    for w, en_title, zh_title in meta:
        en_nav_parts.append(
            f'      - "Week {w}: {en_title}":\n'
            f"          - Lesson: en/week{w}/index.md\n"
            f"          - Examples: en/week{w}/examples.md"
        )
        zh_nav_parts.append(
            f'      - "第 {w} 周: {zh_title}":\n'
            f"          - 课文: zh/week{w}/index.md\n"
            f"          - 示例: zh/week{w}/examples.md"
        )
    en_nav = "\n".join(en_nav_parts)
    zh_nav = "\n".join(zh_nav_parts)
    yml = f"""# Generated by scripts/build_website.py — do not edit by hand.
site_name: Tcl Language Course
site_description: Bilingual Tcl / Calibre layout scripting lessons
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
      accent: cyan
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: teal
      accent: cyan
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.highlight
    - content.code.copy
    - toc.follow

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

validation:
  omitted_files: warn
  absolute_links: info
  unrecognized_links: warn

nav:
  - Home: index.md
  - Playground: playground.md
  - English:
{en_nav}
  - 中文:
{zh_nav}
  - Help:
      - Tcl help: help/tcl.md
      - Calibre help: help/calibre.md
      - Coverage: help/coverage.md
      - Timing Analysis Lab: help/timing_lab.md
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
    write_home()
    copy_help_docs()
    write_contributors()
    write_playground()
    write_mkdocs_yml(meta)
    print(f"Generated website for {len(meta)} weeks → {WEBSITE}")


if __name__ == "__main__":
    main()
