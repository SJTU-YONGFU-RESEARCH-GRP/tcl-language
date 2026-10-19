# Tcl for VLSI · 从基础语法到 DRV 实战应用

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub](https://img.shields.io/badge/GitHub-SJTU--YONGFU--RESEARCH--GRP%2Ftcl--language-181717?logo=github)](https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language)
[![WASM Tcl 8.6](https://img.shields.io/badge/WASM_Tcl-8.6.6_Ready-17776b?logo=webassembly&logoColor=white)](https://sjtu-yongfu-research-grp.github.io/tcl-language/wasm-lab/)
[![DRV-Lite](https://img.shields.io/badge/DRV--Lite-Zero--License_Layout_Sim-0f4f46)](docs/DRVLITE_HELP.md)
[![STA Lab](https://img.shields.io/badge/STA_Lab-Slack_Margin-b96b28)](docs/TIMING_ANALYZER_LAB.md)
[![Bilingual](https://img.shields.io/badge/Bilingual-EN%20%2F%20ZH-blue)](https://sjtu-yongfu-research-grp.github.io/tcl-language/)

Bilingual, beginner-friendly **Tcl educational platform** for learning modern Tcl syntax, data structures, procedures, and understanding how scripting is applied in IC layout and Design Rule Violation (DRV) analysis.

---

## 🌟 核心教学特色与实训工具 (Core Features)

整合来自优秀开源教学实践的核心工具、演练内容与交互设计：

1. **💻 纯客户端 WebAssembly 交互工作坊 (WASM Interactive Lab)**:
   - 内置编译为 WebAssembly 的原生 Tcl 8.6.6 解释器（WACL），零本地环境依赖、零服务器交互，100% 在浏览器安全沙箱中秒级执行。
   - 配备内存变量表格、数据结构单元图谱、执行耗时分析与事件日志输出。
   - [👉 立即在线打开工作坊 (Launch Live WASM Lab)](https://sjtu-yongfu-research-grp.github.io/tcl-language/wasm-lab/)

2. **🎨 典雅学术视觉体系 (Academic Palette)**:
   - 摒弃千篇一律的通用默认样式，定制沉稳学术质感：
     - **底色 (Paper)**: `#f7f6f0`（温暖象牙纸质底色）
     - **主文本 (Ink)**: `#253934`（深邃松烟墨色）
     - **学术主色 (Academic Teal)**: `#17776b`（典雅深青绿）与 `#0f4f46`（沉稳墨绿导航）
     - **重点强调 (Amber)**: `#b96b28`（暖琥珀橙金）
     - **代码底色 (Code Slate)**: `#1d302d`（墨绿极客暗调）
     - **排版字体**: 标题采用经典衬线体 `Georgia, 'Songti SC', 'Noto Serif SC', serif`。

3. **🎯 18 项工程数据练习（54 个阶梯任务）与参考答案**:
   - 涵盖变量置换、列表排序、嵌套字典、正则匹配、文件解析、CSV/JSON 转换到多字段聚合。
   - 预置真实工程练习数据集：`data/chip_runs.csv`、`data/top10_servers.tsv`、`data/wafers.csv`、`data/weather_beijing.json` 等。
   - 配套标准起步模版（`exercises/`）与全套参考解答（`solutions/`）。

4. **🏆 6 大综合数据实战项目 (Capstone Projects A–F)**:
   - **Project A**: Nginx/Apache 访问日志统计与告警过滤
   - **Project B**: 晶圆测试机台良率聚合与缺陷分类
   - **Project C**: Git 代码仓库提交历史度量报告生成
   - **Project D**: 销售与库存多表自动化流水对账
   - **Project E**: 多源 JSON/CSV 跨格式清洗与转换管道
   - **Project F**: EDA 文本报告解析与 DRV 版图违规分析
   - 配备多组断言测试用例（`case-1.tcl` 到 `case-4.tcl`）。

5. **📐 DRV-Lite: 纯 Tcl 版图轻量仿真器**:
   - 无需商业 EDA 许可证！纯 Tcl 实现的 `layout` 对象结构，支持在普通电脑的标准 `tclsh` 环境下操纵多边形、引脚、图层及版图坐标，帮助初学者理解 DRV 版图分析的基本原理。

6. **⚡ STA 静态时序分析入门实验**:
   - 解析数字芯片时序报告（`data/sample_timing.rpt`），计算 Worst Negative Slack (WNS) 与 Total Negative Slack (TNS)，直观理解时序裕量分析与脚本解析方法。

7. **🧠 Tcl 3 步置换心智模型**:
   - 严格遵循 `切分 (Grouping)` $\to$ `置换 (Substitution)` $\to$ `调用 (Invocation)`，帮助初学者彻底理解大括号 `{}` 与双引号 `""` 的差异，掌握花括号 `expr {$a + $b}` 的安全准则。

---

## 🚀 本地快速上手 (Quick Start)

### 1. 环境准备
- **第 1–20 周**: 本地终端安装 [`tclsh`](https://www.tcl.tk/)（Tcl 8.5/8.6/9.0 均可）
- **第 21–40 周**: 商业版 `calibredrv` **或** 纯 Tcl **DRV-Lite 仿真器**（系统自动回退，无需配置）

### 2. 克隆与常用指令

```bash
git clone git@github.com:SJTU-YONGFU-RESEARCH-GRP/tcl-language.git
cd tcl-language

# 检查本地环境与 DRV-Lite 状态
make check-env

# 运行 DRV-Lite 版图仿真器 6 项单元自测
make drvlite-test

# 运行 STA 静态时序分析入门实验
make timing-demo

# 运行第一周范例脚本
make week1-01

# 运行第 21 周版图脚本 (自动调用 DRV-Lite 仿真)
make week21-01

# 运行学生练习答案与项目自测
tclsh solutions/01/01.tcl
(cd capstone/A && tclsh solution.tcl)
```

### 3. 本地启动文档与工作坊站点

```bash
make site-install    # 安装 Python 与 MkDocs 依赖
make site            # 生成全套静态文档与 WASM 工作坊
make site-serve      # 本地预览 http://127.0.0.1:8000
```

---

## 📁 仓库结构全貌 (Repository Layout)

```text
tcl-language/
├── PLAN.md                 # 40 周全体系教学大纲与演进路线
├── Makefile                # 课程运行器、自测脚本与站点构建入口
├── data/                   # 真实工业场景数据集 (晶圆、服务器日志、时序报告)
├── exercises/              # 18 节实战练习起步模版 (54 项编码任务)
├── solutions/              # 18 节实战练习标准参考答案
├── capstone/               # 6 大综合数据工程项目 (A–F，附测试用例)
├── homework/               # GateUltra 贡献的课后练习题集与验证器
├── quiz/                   # thy031 贡献的随堂自测题库
├── lessons/                # 40 周中英双语课文与 100+ 可执行示例脚本
├── examples/               # 包含 timing_report_analyzer.tcl 等工业范例
├── docs/                   # TCL_HELP.md, DRVLITE_HELP.md 等指导文档
├── tools/
│   ├── drvlite/            # DRV-Lite 纯 Tcl Calibre DESIGNrev 版图仿真器
│   └── ...                 # 语法与命令探测工具
└── website/                # MkDocs 站点源文件与 WebAssembly 交互工作坊
    ├── docs/               # 编译后的文档 Markdown
    └── workshop/           # WACL 原生 Tcl 8.6.6 WebAssembly 完整运行时
```

---

## 👥 贡献者致谢 (Contributors)

特别致谢参与建设与创新的师生团队成员（按 GitHub ID 字母排序）：

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
        <sub>@Su3037 (RPG Media)</sub>
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

详见 [`CONTRIBUTORS.md`](CONTRIBUTORS.md) 及线上主站 [贡献者名录](https://sjtu-yongfu-research-grp.github.io/tcl-language/contributors/)。

---

## 📜 许可证 (License)

- 教学文档与课件内容采用 [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) 许可协议。
- 代码脚本与仿真工具采用 [MIT License](LICENSE) 开源协议。
