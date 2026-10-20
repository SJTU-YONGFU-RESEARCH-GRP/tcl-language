# Tcl for VLSI · From Core Syntax to DRV Automation

<p align="center">
  <b>English</b> · 
  <a href="README.zh.md">简体中文</a> · 
  <a href="README.ms.md">Bahasa Melayu</a> · 
  <a href="README.fr.md">Français</a>
</p>

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub](https://img.shields.io/badge/GitHub-SJTU--YONGFU--RESEARCH--GRP%2Ftcl--language-181717?logo=github)](https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language)
[![Web Playground](https://img.shields.io/badge/Playground-Zero--Install-17776b?logo=javascript&logoColor=white)](https://sjtu-yongfu-research-grp.github.io/tcl-language/playground/)
[![DRV-Lite](https://img.shields.io/badge/DRV--Lite-Zero--License_Layout_Sim-0f4f46)](docs/DRVLITE_HELP.md)
[![STA Lab](https://img.shields.io/badge/STA_Lab-Slack_Margin-b96b28)](docs/TIMING_ANALYZER_LAB.md)
[![Multilingual](https://img.shields.io/badge/i18n-EN%20%7C%20ZH%20%7C%20MS%20%7C%20FR-blue)](https://sjtu-yongfu-research-grp.github.io/tcl-language/)

A modern, beginner-friendly **Tcl VLSI Educational Platform** designed to take students from core Tcl scripting syntax and procedural fluency to industrial physical design automation, Design Rule Violation (DRV) analysis, and Static Timing Analysis (STA) sign-off.

---

## 🌟 Core Educational Features & Practical Tools

Developed at Shanghai Jiao Tong University (SJTU) and open-sourced for the global semiconductor community, this platform integrates cutting-edge pedagogical tools:

1. **⚡ Zero-Install In-Browser Web Playground**:
   - Pure client-side WebAssembly execution with zero server overhead and zero local configuration.
   - Built-in templates for Welch's 3-step substitution model, safe `expr`, list/dict manipulation, STA timing report parsing, and DRV-Lite layout scripting.
   - [👉 Launch the Web Playground](https://sjtu-yongfu-research-grp.github.io/tcl-language/playground/)

2. **📐 DRV-Lite: Pure-Tcl IC Layout Simulator & In-Browser Visualizer**:
   - Zero commercial EDA licensing required! A lightweight `layout` object hierarchy implemented entirely in standard Tcl for manipulating cells, layers, polygons, wires, and bounding boxes.
   - Paired with an interactive [📐 2D VLSI Layout Visualizer](https://sjtu-yongfu-research-grp.github.io/tcl-language/help/layout_viewer/) supporting panning, zooming, and a live CalibreDRV CLI console supporting commands like `create`, `delete`, `bbox`, `iterator count`, `shift`, and `scale`.

3. **⚡ STA Static Timing Analysis & Tapeout Gatekeeper**:
   - Parses real-world digital IC timing reports (`data/sample_timing.rpt`) and calculates Worst Negative Slack (WNS) and Total Negative Slack (TNS).
   - Paired with the interactive [⚡ STA Timing Slack Gatekeeper](https://sjtu-yongfu-research-grp.github.io/tcl-language/help/timing_calculator/) to dynamically experiment with clock period, data path delay, and jitter to visualize tapeout sign-off criteria.

4. **🎯 18 Practical Engineering Data Exercises (54 Tiered Tasks)**:
   - Covers variable substitution, list sorting, nested dictionaries, regular expression matching, file channels, CSV/JSON format conversion, and multi-field data aggregation.
   - Includes real industrial datasets: `data/chip_runs.csv`, `data/top10_servers.tsv`, `data/wafers.csv`, `data/weather_beijing.json`, and more.
   - Starter exercise templates (`exercises/`) and full verified reference solutions (`solutions/`).

5. **🏆 6 Capstone Data Engineering Projects (Projects A–F)**:
   - **Project A**: Nginx/Apache Web Server Access Log Analytics & Alerting
   - **Project B**: Automated Wafer Sort Yield Aggregator & Defect Binning
   - **Project C**: Git Repository Commit Velocity & Churn Reporting
   - **Project D**: Multi-Table Sales & Inventory Reconciliation Pipeline
   - **Project E**: Multi-Source JSON/CSV Cleansing & ETL Transformation
   - **Project F**: EDA Timing Report Parsing & DRV Layout Violation Audit
   - Fully validated with automated assertion testbenches (`case-1.tcl` to `case-4.tcl`).

6. **🧠 Tcl 3-Step Mental Model**:
   - Strict adherence to `Grouping` $\to$ `Substitution` $\to$ `Invocation`, demystifying curly braces `{}` vs double quotes `""`, and enforcing the secure braces rule for `expr {$a + $b}`.

7. **🎯 Quiz Challenges & Public Leaderboard**:
   - 4 modular diagnostic quizzes with verifiable cryptographic certificate generation and real-time community leaderboard benchmarking.

---

## 📚 40-Lesson Curriculum Roadmap

- **M10: Tcl Core Syntax (Lessons 01–10)**: Fundamental commands, variables, control flow, procedures (`proc`), lists, and the 3-step evaluation model.
- **M20: Fluency & Tool Glue (Lessons 11–20)**: Dictionaries (`dict`), robust file I/O, regular expressions, namespaces (`namespace`), and object-oriented programming with `TclOO`.
- **M30: Calibre Layout Core (Lessons 21–30)**: Pure-Tcl DRV-Lite simulator, layer instantiation, geometry polygons, and CalibreDRV CLI commands.
- **M40: Physical Design Automation & Sign-Off (Lessons 31–40)**: Static timing analysis, DEF/LEF parsing, DRV violation audits, and automated ECO routing fixes.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Lessons 01–20**: Local terminal with standard [`tclsh`](https://www.tcl.tk/) (Tcl 8.5, 8.6, or 9.0).
- **Lessons 21–40**: Commercial `calibredrv` **or** the bundled pure-Tcl **DRV-Lite simulator** (automatic fallback, no setup needed).

### 2. Clone & Verification Commands

```bash
git clone https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language.git
cd tcl-language

# Check local environment and DRV-Lite status
make check-env

# Run 6 unit tests on the DRV-Lite layout simulator
make drvlite-test

# Run the Static Timing Analysis (STA) report parser demo
make timing-demo

# Run the Lesson 1 starter example
make week1-01

# Run the Lesson 21 layout script (uses DRV-Lite simulation)
make week21-01

# Run student exercise solutions and capstone testbenches
tclsh solutions/01/01.tcl
(cd capstone/A && tclsh solution.tcl)
```

### 3. Build & Preview Website Locally

```bash
make site-install    # Install Python & MkDocs dependencies
make site            # Build static docs and multilingual sites
make site-serve      # Preview locally at http://127.0.0.1:8000
```

---

## 📁 Repository Layout

```text
tcl-language/
├── PLAN.md                 # 40-week curriculum syllabus and milestone roadmap
├── Makefile                # Course test runner, demo entry points, and site builder
├── data/                   # Realistic industrial datasets (wafers, logs, STA reports)
├── exercises/              # 18 lab exercise starter templates (54 tasks)
├── solutions/              # 18 official reference solutions
├── capstone/               # 6 capstone data engineering projects (A–F with test cases)
├── homework/               # Homework problem sets and automated validators
├── quiz/                   # Chapter quizzes and certification challenges
├── lessons/                # 40 bilingual lessons and 100+ executable Tcl scripts
├── examples/               # Industrial examples (e.g. timing_report_analyzer.tcl)
├── docs/                   # Guides (TCL_HELP.md, DRVLITE_HELP.md, etc.)
├── tools/
│   ├── drvlite/            # Pure-Tcl Calibre DESIGNrev layout simulator
│   └── ...                 # Syntax probes and introspection utilities
└── website/                # MkDocs documentation source files & i18n configs
```

---

## 👥 Contributors & Attribution

Special thanks to the instructors, researchers, and student developers (in alphabetical order by GitHub handle):

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/yongfu-li">
        <img src="https://avatars.githubusercontent.com/u/10367890?v=4" width="80" height="80" alt="yongfu-li"/><br/>
        <sub><b>Li Yongfu</b></sub><br/>
        <sub>@yongfu-li</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Capeur">
        <img src="https://avatars.githubusercontent.com/u/197603203?v=4" width="80" height="80" alt="Capeur"/><br/>
        <sub><b>David MUY</b></sub><br/>
        <sub>@Capeur</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/FanqinZeng">
        <img src="https://avatars.githubusercontent.com/u/151010024?v=4" width="80" height="80" alt="FanqinZeng"/><br/>
        <sub><b>FanQin Zeng</b></sub><br/>
        <sub>@FanqinZeng (WASM & Exercises)</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/GateUltra">
        <img src="https://avatars.githubusercontent.com/u/138369042?v=4" width="80" height="80" alt="GateUltra"/><br/>
        <sub><b>GateUltra</b></sub><br/>
        <sub>@GateUltra (Homeworks)</sub>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/muranfei">
        <img src="https://avatars.githubusercontent.com/u/31174606?v=4" width="80" height="80" alt="muranfei"/><br/>
        <sub><b>muranfei</b></sub><br/>
        <sub>@muranfei</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/stephQ-lab">
        <img src="https://avatars.githubusercontent.com/u/186373504?v=4" width="80" height="80" alt="stephQ-lab"/><br/>
        <sub><b>stephQ-lab</b></sub><br/>
        <sub>@stephQ-lab</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Su3037">
        <img src="https://avatars.githubusercontent.com/u/154591477?v=4" width="80" height="80" alt="Su3037"/><br/>
        <sub><b>Supan</b></sub><br/>
        <sub>@Su3037</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/thy031">
        <img src="https://avatars.githubusercontent.com/u/188567228?v=4" width="80" height="80" alt="thy031"/><br/>
        <sub><b>thy031</b></sub><br/>
        <sub>@thy031 (Quizzes)</sub>
      </a>
    </td>
  </tr>
</table>

See [`CONTRIBUTORS.md`](CONTRIBUTORS.md) and the online [Contributors Directory](https://sjtu-yongfu-research-grp.github.io/tcl-language/contributors/).

---

## 📜 License

- Curriculum text, tutorials, and documentation are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
- Source code scripts, simulators, and testbenches are licensed under the [MIT License](LICENSE).
