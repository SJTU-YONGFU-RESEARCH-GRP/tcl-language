#!/usr/bin/env python3
"""VLSI & Tcl Terminology Glossary generator for Tcl for VLSI Portal.

Extracts structured term definitions from Capeur's YAML glossary
(dodekalogue, standard cells, design rules, bounding boxes, etc.)
and generates an interactive, searchable bilingual reference portal.
"""

from __future__ import annotations
from pathlib import Path
import yaml
import html

ROOT = Path(__file__).resolve().parent.parent

CATEGORY_MAP = {
    # VLSI Physical Design & Calibre
    "abut": ("VLSI & Layout", "版图与物理设计"),
    "block": ("VLSI & Layout", "版图与物理设计"),
    "bounding-box": ("VLSI & Layout", "版图与物理设计"),
    "channel": ("VLSI & Layout", "版图与物理设计"),
    "chip": ("VLSI & Layout", "版图与物理设计"),
    "coordinate": ("VLSI & Layout", "版图与物理设计"),
    "design-rule": ("VLSI & Layout", "版图与物理设计"),
    "drv-lite": ("VLSI & Layout", "版图与物理设计"),
    "floorplan": ("VLSI & Layout", "版图与物理设计"),
    "gds": ("VLSI & Layout", "版图与物理设计"),
    "klayout": ("VLSI & Layout", "版图与物理设计"),
    "layer": ("VLSI & Layout", "版图与物理设计"),
    "layer-purpose": ("VLSI & Layout", "版图与物理设计"),
    "layout": ("VLSI & Layout", "版图与物理设计"),
    "micrometre": ("VLSI & Layout", "版图与物理设计"),
    "pitch": ("VLSI & Layout", "版图与物理设计"),
    "square-micrometre": ("VLSI & Layout", "版图与物理设计"),
    "standard-cell": ("VLSI & Layout", "版图与物理设计"),
    "vlsi": ("VLSI & Layout", "版图与物理设计"),
    "wafer": ("VLSI & Layout", "版图与物理设计"),
    "wire": ("VLSI & Layout", "版图与物理设计"),
    "calibre": ("VLSI & Layout", "版图与物理设计"),

    # Data Structures & Types
    "array": ("Data Structures", "数据结构与类型"),
    "datatype": ("Data Structures", "数据结构与类型"),
    "decimal-number": ("Data Structures", "数据结构与类型"),
    "dictionary": ("Data Structures", "数据结构与类型"),
    "element": ("Data Structures", "数据结构与类型"),
    "format-specifier": ("Data Structures", "数据结构与类型"),
    "index": ("Data Structures", "数据结构与类型"),
    "insertion-order": ("Data Structures", "数据结构与类型"),
    "integer": ("Data Structures", "数据结构与类型"),
    "integer-division": ("Data Structures", "数据结构与类型"),
    "key": ("Data Structures", "数据结构与类型"),
    "list": ("Data Structures", "数据结构与类型"),
    "literal": ("Data Structures", "数据结构与类型"),
    "nested-list": ("Data Structures", "数据结构与类型"),
    "regular-expression": ("Data Structures", "数据结构与类型"),
    "remainder": ("Data Structures", "数据结构与类型"),
    "separator": ("Data Structures", "数据结构与类型"),
    "string": ("Data Structures", "数据结构与类型"),
    "value": ("Data Structures", "数据结构与类型"),

    # Control Flow & Scope
    "branch": ("Control Flow", "流程控制与作用域"),
    "comparison-operator": ("Control Flow", "流程控制与作用域"),
    "condition": ("Control Flow", "流程控制与作用域"),
    "counter": ("Control Flow", "流程控制与作用域"),
    "error-message": ("Control Flow", "流程控制与作用域"),
    "guard-clause": ("Control Flow", "流程控制与作用域"),
    "infinite-loop": ("Control Flow", "流程控制与作用域"),
    "loop": ("Control Flow", "流程控制与作用域"),
    "loop-body": ("Control Flow", "流程控制与作用域"),
    "loop-variable": ("Control Flow", "流程控制与作用域"),
    "stack-trace": ("Control Flow", "流程控制与作用域"),

    # Tools & Runtime
    "capstone": ("Tools & Runtime", "工具与运行环境"),
    "playground": ("Tools & Runtime", "工具与运行环境"),
    "tclsh": ("Tools & Runtime", "工具与运行环境"),
}


def load_glossary_terms() -> list[dict]:
    # Look in data/glossary within repository first
    glossary_dir = ROOT / "data" / "glossary"
    if not glossary_dir.exists():
        glossary_dir = ROOT.parent / "projects" / "capeur" / "src" / "content" / "glossary"
    if not glossary_dir.exists():
        glossary_dir = ROOT / "docs" / "glossary"
    
    terms = []
    if glossary_dir.exists():
        for p in sorted(glossary_dir.glob("*.yaml")):
            if p.name.startswith("."):
                continue
            try:
                data = yaml.safe_load(p.read_text(encoding="utf-8"))
                if data and "term" in data:
                    t_name = str(data["term"]).strip()
                    cat_en, cat_zh = CATEGORY_MAP.get(t_name, ("Tcl Syntax & Core", "Tcl 核心语法"))
                    data["cat_en"] = cat_en
                    data["cat_zh"] = cat_zh
                    terms.append(data)
            except Exception:
                continue
    return terms


def write_glossary_pages(docs_dir: Path) -> None:
    terms = load_glossary_terms()
    help_dir = docs_dir / "help"
    help_dir.mkdir(parents=True, exist_ok=True)

    if not terms:
        print("Warning: No glossary YAML files found, generating fallback glossary.")
        terms = [
            {
                "term": "standard-cell",
                "short": "A small, ready-made building block of a chip, such as an inverter (INV) or NAND gate.",
                "long": "A cell library has hundreds of standard cells. They all have the same height and different widths, so they can sit side by side in rows.",
                "see_also": ["block", "layout"],
                "first_taught": "m10-w06-lab",
                "cat_en": "VLSI & Layout",
                "cat_zh": "版图与物理设计",
            },
            {
                "term": "dodekalogue",
                "short": "The 12 core rules defining Tcl syntax and evaluation semantics.",
                "long": "Every Tcl command is evaluated according to the twelve rules of the Tcl syntax dodekalogue.",
                "see_also": ["expr", "substitution"],
                "first_taught": "m10-w01-lab",
                "cat_en": "Tcl Syntax & Core",
                "cat_zh": "Tcl 核心语法",
            },
        ]

    en_content = _build_glossary_page(terms, "en")
    zh_content = _build_glossary_page(terms, "zh")
    ms_content = _build_glossary_page(terms, "ms")
    fr_content = _build_glossary_page(terms, "fr")

    (help_dir / "glossary.md").write_text(en_content, encoding="utf-8")
    (help_dir / "glossary.zh.md").write_text(zh_content, encoding="utf-8")
    (help_dir / "glossary.ms.md").write_text(ms_content, encoding="utf-8")
    (help_dir / "glossary.fr.md").write_text(fr_content, encoding="utf-8")
    print(f"Generated bilingual glossary ({len(terms)} terms) -> {help_dir / 'glossary.md'}")


def _build_glossary_page(terms: list[dict], lang: str) -> str:
    i18n = {
        "en": {
            "title": "📚 VLSI & Tcl Terminology Glossary",
            "badges": ["82 Curated Terms", "VLSI Physical Design", "Tcl Dodekalogue", "Source: Capeur"],
            "desc": "An authoritative bilingual encyclopedia bridging Tcl programming mechanics with semiconductor physical design, standard cells, GDSII layout geometry, and DRC/LVS automation.",
            "search_ph": "Search terms (e.g., standard-cell, dodekalogue, bounding-box, expr)...",
            "all_cat": "All Terms",
            "vlsi_cat": "VLSI & Layout",
            "syntax_cat": "Tcl Syntax & Core",
            "data_cat": "Data Structures",
            "flow_cat": "Control Flow",
            "first_taught": "First Taught",
            "see_also": "See Also",
            "no_match": "No matching terms found. Try clearing the search filter."
        },
        "zh": {
            "title": "📚 芯片物理设计与 Tcl 术语词典 (Glossary)",
            "badges": ["82 个核心术语", "VLSI 物理版图", "Tcl 十二法则", "来源：Capeur"],
            "desc": "汇聚 Tcl 核心置换法则、数据结构与芯片物理版图设计（标准单元、GDSII 几何图元、DRC/LVS 物理验证）的权威中英双语专业词典。",
            "search_ph": "搜索术语 (例如: standard-cell, dodekalogue, bounding-box, expr)...",
            "all_cat": "全部术语",
            "vlsi_cat": "版图与物理设计",
            "syntax_cat": "Tcl 核心语法",
            "data_cat": "数据结构与类型",
            "flow_cat": "流程控制与作用域",
            "first_taught": "首次讲授",
            "see_also": "关联术语",
            "no_match": "未找到匹配术语，请尝试清空搜索关键字。"
        },
        "ms": {
            "title": "📚 Glosari Istilah VLSI & Penskripan Tcl",
            "badges": ["82 Istilah Terpilih", "Reka Bentuk Fizikal VLSI", "Dodekalog Tcl", "Sumber: Capeur"],
            "desc": "Ensiklopedia dwibahasa berwibawa yang merapatkan mekanik penskripan Tcl dengan reka bentuk fizikal semikonduktor, sel piawai, geometri GDSII, dan automasi DRC.",
            "search_ph": "Cari istilah (cth: standard-cell, dodekalogue, bounding-box, expr)...",
            "all_cat": "Semua Istilah",
            "vlsi_cat": "VLSI & Susun Atur",
            "syntax_cat": "Sintaks & Teras Tcl",
            "data_cat": "Struktur Data",
            "flow_cat": "Aliran Kawalan",
            "first_taught": "Mula Diajar",
            "see_also": "Lihat Juga",
            "no_match": "Tiada istilah yang sepadan. Cuba kosongkan carian anda."
        },
        "fr": {
            "title": "📚 Glossaire Terminologique VLSI & Tcl",
            "badges": ["82 Termes Structurés", "Conception Physique VLSI", "Dodécalogue Tcl", "Source: Capeur"],
            "desc": "Encyclopédie bilingue de référence reliant la syntaxe Tcl à la conception physique des semi-conducteurs, cellules standard, géométrie de layout GDSII et vérification DRC.",
            "search_ph": "Rechercher des termes (ex: standard-cell, dodekalogue, bounding-box, expr)...",
            "all_cat": "Tous les Termes",
            "vlsi_cat": "VLSI & Layout",
            "syntax_cat": "Syntaxe & Base Tcl",
            "data_cat": "Structures de Données",
            "flow_cat": "Flux de Contrôle",
            "first_taught": "Première Mention",
            "see_also": "Voir Aussi",
            "no_match": "Aucun terme correspondant. Essayez de réinitialiser la recherche."
        }
    }
    t = i18n.get(lang, i18n["en"])

    cards_html = []
    for item in terms:
        name = html.escape(str(item.get("term", "")))
        short_def = html.escape(str(item.get("short", "")))
        long_def = html.escape(str(item.get("long", "")))
        first_taught = html.escape(str(item.get("first_taught", "")))
        cat = item.get("cat_zh" if lang == "zh" else "cat_en", "Tcl Core")
        cat_key = item.get("cat_en", "Tcl Syntax & Core")

        see_also_chips = []
        for s in item.get("see_also", []) or []:
            s_clean = html.escape(str(s).strip())
            see_also_chips.append(f'<span class="tcl-glossary-tag" onclick="filterByTag(\'{s_clean}\')">{s_clean}</span>')
        see_also_html = " ".join(see_also_chips) if see_also_chips else "—"

        cards_html.append(f"""
<div class="tcl-glossary-card" data-term="{name.lower()}" data-category="{cat_key}" data-search="{name.lower()} {short_def.lower()} {long_def.lower()}">
  <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; flex-wrap: wrap; margin-bottom: 8px;">
    <h3 style="margin: 0; font-size: 1.15rem; font-weight: 800; color: var(--tcl-heading); font-family: 'JetBrains Mono', monospace;">{name}</h3>
    <span class="tcl-badge blue" style="font-size: 11px;">{cat}</span>
  </div>
  <div style="font-size: 13.5px; font-weight: 600; color: var(--tcl-blue-600); margin-bottom: 8px; line-height: 1.5;">{short_def}</div>
  <div style="font-size: 13px; color: var(--md-default-fg-color--light); line-height: 1.6; margin-bottom: 12px;">{long_def}</div>
  <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--tcl-border); padding-top: 10px; font-size: 12px; color: var(--md-default-fg-color--lighter); flex-wrap: wrap; gap: 8px;">
    <div><strong>{t['first_taught']}:</strong> <code style="font-size:11px;">{first_taught}</code></div>
    <div style="display: flex; gap: 4px; align-items: center; flex-wrap: wrap;"><strong>{t['see_also']}:</strong> {see_also_html}</div>
  </div>
</div>
""")

    cards_joined = "\n".join(cards_html)

    badges_html = "\n".join([f'  <span class="tcl-badge blue">{b}</span>' for b in t["badges"]])

    return f"""# {t['title']}

<div class="tcl-badge-cluster">
{badges_html}
</div>

{t['desc']}

---

<!-- Search & Category Filters -->
<div style="background: var(--tcl-surface); border: 1px solid var(--tcl-border); border-radius: 12px; padding: 18px; margin: 20px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
  <div style="margin-bottom: 12px;">
    <input type="text" id="glossarySearchInput" oninput="filterGlossary()" placeholder="{t['search_ph']}" style="width: 100%; padding: 10px 14px; border: 1px solid var(--tcl-border); border-radius: 8px; background: var(--md-default-bg-color); color: var(--tcl-heading); font-size: 14px; outline: none;">
  </div>
  <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
    <span style="font-size: 12.5px; font-weight: 700; color: var(--tcl-heading);">Filter:</span>
    <button onclick="setCategoryFilter('all')" class="tcl-btn tcl-btn-primary tcl-filter-btn active" data-cat="all" style="padding: 4px 10px; font-size: 12px;">{t['all_cat']}</button>
    <button onclick="setCategoryFilter('VLSI & Layout')" class="tcl-btn tcl-btn-secondary tcl-filter-btn" data-cat="VLSI & Layout" style="padding: 4px 10px; font-size: 12px;">{t['vlsi_cat']}</button>
    <button onclick="setCategoryFilter('Tcl Syntax & Core')" class="tcl-btn tcl-btn-secondary tcl-filter-btn" data-cat="Tcl Syntax & Core" style="padding: 4px 10px; font-size: 12px;">{t['syntax_cat']}</button>
    <button onclick="setCategoryFilter('Data Structures')" class="tcl-btn tcl-btn-secondary tcl-filter-btn" data-cat="Data Structures" style="padding: 4px 10px; font-size: 12px;">{t['data_cat']}</button>
    <button onclick="setCategoryFilter('Control Flow')" class="tcl-btn tcl-btn-secondary tcl-filter-btn" data-cat="Control Flow" style="padding: 4px 10px; font-size: 12px;">{t['flow_cat']}</button>
  </div>
</div>

<div id="glossaryCount" style="font-size: 13px; color: var(--md-default-fg-color--lighter); margin-bottom: 16px; font-weight: 600;">Showing {len(terms)} terms</div>

<div id="glossaryCardsGrid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
{cards_joined}
</div>

<div id="glossaryNoMatch" style="display: none; text-align: center; padding: 40px 20px; color: var(--md-default-fg-color--lighter); font-size: 14px;">
  {t['no_match']}
</div>

<style>
.tcl-glossary-card {{
  background: var(--tcl-surface);
  border: 1px solid var(--tcl-border);
  border-radius: 10px;
  padding: 18px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.04);
  transition: transform 0.2s, border-color 0.2s;
}}
.tcl-glossary-card:hover {{
  transform: translateY(-2px);
  border-color: var(--tcl-blue-600);
}}
.tcl-glossary-tag {{
  display: inline-block;
  padding: 2px 6px;
  background: rgba(56, 189, 248, 0.1);
  color: var(--tcl-blue-600);
  border-radius: 4px;
  font-size: 11px;
  font-family: monospace;
  cursor: pointer;
  transition: background 0.2s;
}}
.tcl-glossary-tag:hover {{
  background: rgba(56, 189, 248, 0.25);
}}
.tcl-filter-btn.active {{
  background: var(--tcl-blue-600) !important;
  color: #fff !important;
  border-color: var(--tcl-blue-600) !important;
}}
</style>

<script>
let currentCategory = 'all';

function filterGlossary() {{
  const query = (document.getElementById('glossarySearchInput').value || '').trim().toLowerCase();
  const cards = document.querySelectorAll('.tcl-glossary-card');
  let visibleCount = 0;

  cards.forEach(card => {{
    const searchData = card.getAttribute('data-search') || '';
    const cat = card.getAttribute('data-category') || '';
    
    const matchesQuery = !query || searchData.includes(query);
    const matchesCat = (currentCategory === 'all') || (cat === currentCategory);

    if (matchesQuery && matchesCat) {{
      card.style.display = 'block';
      visibleCount++;
    }} else {{
      card.style.display = 'none';
    }}
  }});

  document.getElementById('glossaryCount').innerText = `Showing ${{visibleCount}} of ${{cards.length}} terms`;
  document.getElementById('glossaryNoMatch').style.display = visibleCount === 0 ? 'block' : 'none';
}}

function setCategoryFilter(cat) {{
  currentCategory = cat;
  document.querySelectorAll('.tcl-filter-btn').forEach(btn => {{
    if (btn.getAttribute('data-cat') === cat) {{
      btn.classList.add('active');
    }} else {{
      btn.classList.remove('active');
    }}
  }});
  filterGlossary();
}}

function filterByTag(tagName) {{
  document.getElementById('glossarySearchInput').value = tagName;
  setCategoryFilter('all');
  window.scrollTo({{ top: 120, behavior: 'smooth' }});
}}
</script>
"""
