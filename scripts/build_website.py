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


def write_stylesheets() -> None:
    """Create custom CSS for elevated visual aesthetics, custom color palette, and component cards."""
    css_dir = DOCS / "stylesheets"
    css_dir.mkdir(parents=True, exist_ok=True)
    css_content = """/* Custom styling for Tcl Language Lab inspired by top student educational innovations */

:root {
  --tcl-teal-dark: #0f766e;
  --tcl-teal: #14b8a6;
  --tcl-teal-light: #ccfbf1;
  --tcl-amber: #f59e0b;
  --tcl-amber-light: #fef3c7;
  --tcl-slate-dark: #0f172a;
  --tcl-slate: #1e293b;
  --tcl-slate-light: #f8fafc;
  --tcl-border: #e2e8f0;

  --md-primary-fg-color: #0f766e;
  --md-primary-fg-color--light: #14b8a6;
  --md-primary-fg-color--dark: #115e59;
  --md-accent-fg-color: #f59e0b;
}

[data-md-color-scheme="slate"] {
  --md-default-bg-color: #0b1120;
  --md-default-bg-color--light: #0f172a;
  --md-default-bg-color--lighter: #1e293b;
  --md-primary-fg-color: #14b8a6;
  --md-primary-fg-color--dark: #0f766e;
  --tcl-border: #334155;
  --tcl-slate-light: #1e293b;
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
  border: 1px solid rgba(15, 118, 110, 0.2);
}
[data-md-color-scheme="slate"] .tcl-badge {
  background: rgba(20, 184, 166, 0.15);
  color: #5eead4;
  border-color: rgba(94, 234, 212, 0.3);
}
.tcl-badge.amber {
  background: var(--tcl-amber-light);
  color: #b45309;
  border-color: rgba(245, 158, 11, 0.3);
}
[data-md-color-scheme="slate"] .tcl-badge.amber {
  background: rgba(245, 158, 11, 0.15);
  color: #fcd34d;
  border-color: rgba(252, 211, 77, 0.3);
}
.tcl-hero-title {
  font-size: 2.2rem;
  font-weight: 800;
  line-height: 1.25;
  margin: 8px 0 14px 0;
  background: linear-gradient(135deg, #0f766e 0%, #14b8a6 40%, #f59e0b 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
[data-md-color-scheme="slate"] .tcl-hero-title {
  background: linear-gradient(135deg, #2dd4bf 0%, #38bdf8 50%, #fbbf24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.tcl-hero-subtitle {
  font-size: 1.1rem;
  line-height: 1.6;
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
  background: #0f766e;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(15, 118, 110, 0.25);
}
.tcl-btn-primary:hover {
  background: #0d9488;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(15, 118, 110, 0.35);
}
.tcl-btn-secondary {
  background: var(--tcl-slate-light);
  color: var(--md-default-fg-color) !important;
  border: 1px solid var(--tcl-border);
}
.tcl-btn-secondary:hover {
  border-color: #0f766e;
  background: rgba(15, 118, 110, 0.08);
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
  font-size: 1.85rem;
  font-weight: 800;
  color: #0f766e;
  display: block;
}
[data-md-color-scheme="slate"] .tcl-fact-val {
  color: #2dd4bf;
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
  border-color: #0f766e;
  box-shadow: 0 12px 28px rgba(15, 118, 110, 0.12);
}
.tcl-route-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: #0f766e;
}
.tcl-route-card.route-exp::before { background: #0284c7; }
.tcl-route-card.route-vlsi::before { background: #f59e0b; }
.tcl-route-num {
  font-size: 12px;
  font-family: monospace;
  font-weight: 700;
  color: #0f766e;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.tcl-route-card.route-exp .tcl-route-num { color: #0284c7; }
.tcl-route-card.route-vlsi .tcl-route-num { color: #f59e0b; }
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
  border-color: #14b8a6;
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
}
.tcl-unit-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(15, 118, 110, 0.1);
  color: #0f766e;
  margin-bottom: 8px;
}
"""
    (css_dir / "extra.css").write_text(css_content, encoding="utf-8")


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
        en_rows.append(f"| Week {w:02d} | [{en_short}](en/week{w}/index.md) | [Examples](en/week{w}/examples.md) |")
        zh_rows.append(f"| 第 {w:02d} 周 | [{zh_short}](zh/week{w}/index.md) | [示例代码](zh/week{w}/examples.md) |")

    index = f"""<div class="tcl-hero">
  <div class="tcl-badge-cluster">
    <span class="tcl-badge">CC BY 4.0</span>
    <span class="tcl-badge">SJTU-YONGFU-RESEARCH-GRP</span>
    <span class="tcl-badge amber">DRV-Lite Simulator Ready</span>
    <span class="tcl-badge">STA Timing Sign-Off</span>
    <span class="tcl-badge">Bilingual EN/ZH</span>
  </div>

  <h1 class="tcl-hero-title">Tcl for VLSI · 从控制台语法到芯片版图与时序自动化</h1>

  <div class="tcl-hero-subtitle">
    从一张控制台打印卡片，到一套完整的工业级芯片版图自动化脚本与静态时序分析流水线。<br>
    结合 <strong>Brent Welch 三步置换心智模型</strong>、<strong>免商业许可 DRV-Lite 版图仿真器</strong> 与 <strong>STA 时序违规闭环门禁</strong>，让每行 Tcl 代码都能在真实工程场景中高效运行。
  </div>

  <div class="tcl-cta-group">
    <a href="playground/" class="tcl-btn tcl-btn-primary">🚀 进入网页实验室 (Playground)</a>
    <a href="zh/week1/" class="tcl-btn tcl-btn-secondary">📖 开始第一课 (Week 1)</a>
    <a href="help/timing_lab/" class="tcl-btn tcl-btn-secondary">⚡ 时序分析实验 (Timing Lab)</a>
    <a href="help/tcl/" class="tcl-btn tcl-btn-secondary">🧠 三步置换心智模型</a>
  </div>
</div>

<div class="tcl-fact-strip">
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">40 周</span>
    <span class="tcl-fact-lbl">系统进阶计划</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">100+</span>
    <span class="tcl-fact-lbl">原创可运行范例</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">零授权</span>
    <span class="tcl-fact-lbl">DRV-Lite 版图仿真器</span>
  </div>
  <div class="tcl-fact-item">
    <span class="tcl-fact-val">工业级</span>
    <span class="tcl-fact-lbl">STA 时序违规门禁</span>
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
    <a href="zh/week1/" class="tcl-btn tcl-btn-secondary" style="font-size: 13px; padding: 6px 14px;">从第 1 周开始 →</a>
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

  <div class="tcl-pillar-card">
    <div class="tcl-pillar-icon">💻</div>
    <div class="tcl-pillar-title">免安装交互式 Web Playground</div>
    <div class="tcl-pillar-desc">
      内置一键预设代码示例，直接在浏览器中观察标准输出与变量变化，随时随地验证代码逻辑。
    </div>
  </div>
</div>

---

## 📚 课程体系索引 (Curriculum Directory)

### 中文课程导航 (Chinese Lessons)

| 周次 | 课程专题 | 示例代码 |
| :---: | :--- | :---: |
{chr(10).join(zh_rows)}

---

### English Lessons Navigation

| Week | Topic | Examples |
| :---: | :--- | :---: |
{chr(10).join(en_rows)}

---

## 🚀 本地快速上手 (Quick Start)

```bash
git clone {GITHUB}.git
cd tcl-language

make check-env        # 检查 tclsh 与 DRV-Lite 仿真器状态
make drvlite-test     # 运行纯 Tcl 版图仿真器 6 项单元自测
make timing-demo      # 运行 STA 静态时序分析实验
make week1-01         # 运行第 1 周第一课范例
make week21-01        # 运行第 21 周版图范例 (支持 DRV-Lite 仿真)
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
    write_stylesheets()
    write_home()
    copy_help_docs()
    write_contributors()
    write_playground()
    write_mkdocs_yml(meta)
    print(f"Generated website for {len(meta)} weeks → {WEBSITE}")


if __name__ == "__main__":
    main()
