# tcl-language

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub](https://img.shields.io/badge/GitHub-SJTU--YONGFU--RESEARCH--GRP%2Ftcl--language-181717?logo=github)](https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language)

Bilingual **Tcl-first** curriculum for learning Tcl syntax, TclOO, and Calibre DESIGNrev (`calibredrv`) layout scripting — weekly lessons, runnable examples, and a MkDocs site.

**Repository:** [SJTU-YONGFU-RESEARCH-GRP/tcl-language](https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language)

- **Organization**: [SJTU-YONGFU-RESEARCH-GRP](https://github.com/SJTU-YONGFU-RESEARCH-GRP)
- **Course website**: https://sjtu-yongfu-research-grp.github.io/tcl-language/
- **Plan / roadmap**: [PLAN.md](PLAN.md)
- **Lesson index**: [lessons/README.md](lessons/README.md)
- **License**: CC BY 4.0 (see [`LICENSE`](LICENSE))

## Table of contents

- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Project layout](#project-layout)
- [Contributors](#contributors)
- [License](#license)
- [Contact](#contact)

## Requirements

- **Weeks 1–20**: [`tclsh`](https://www.tcl.tk/) on your `PATH`
- **Weeks 21+**: Calibre DESIGNrev (`calibredrv`) via [`scripts/run_calibre_tcl.sh`](scripts/run_calibre_tcl.sh) (see [`scripts/setup_calibredrv.sh`](scripts/setup_calibredrv.sh))
- **Optional site**: Python + MkDocs (`make site-install`, then `make site` / `make site-serve`)

## Quick start

```bash
git clone https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language.git
cd tcl-language

make help              # list targets and milestones
make check             # verify tclsh
make week1-01          # first Week 1 example (tclsh)
make week21-01         # first Calibre week (needs calibredrv)
make milestones        # print roadmap
make help-tcl          # Tcl discovery tips
make help-calibre      # Calibre Usage tips
```

Help docs: [docs/TCL_HELP.md](docs/TCL_HELP.md) · [docs/CALIBRE_HELP.md](docs/CALIBRE_HELP.md) · [docs/COVERAGE.md](docs/COVERAGE.md)

## Project layout

```text
tcl-language/
├── PLAN.md                 # 40-week curriculum plan
├── Makefile                # week runners and site targets
├── lessons/                # bilingual lessons + .tcl examples
├── examples/               # Calibre / demo scripts
├── docs/                   # coverage and help notes
├── scripts/                # calibredrv wrappers and helpers
├── tools/                  # Tcl/Calibre help probes
└── website/                # MkDocs lesson site
```

## Contributors

Collaborators on this repository. Also listed in [`CONTRIBUTORS.md`](CONTRIBUTORS.md) and on the course site: [Contributors](https://sjtu-yongfu-research-grp.github.io/tcl-language/contributors/).

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
        <sub>@FanqinZeng</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/GateUltra">
        <img src="https://avatars.githubusercontent.com/u/138369042?v=4" width="80" height="80" alt="GateUltra"/><br/>
        <sub><b>GateUltra</b></sub><br/>
        <sub>@GateUltra</sub>
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
        <img src="https://avatars.githubusercontent.com/u/330705434?v=4" width="80" height="80" alt="thy031"/><br/>
        <sub><b>thy031</b></sub><br/>
        <sub>@thy031</sub>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/xingguangyaoyu">
        <img src="https://avatars.githubusercontent.com/u/170154323?v=4" width="80" height="80" alt="xingguangyaoyu"/><br/>
        <sub><b>xingguangyaoyu</b></sub><br/>
        <sub>@xingguangyaoyu</sub>
      </a>
    </td>
  </tr>
</table>

| Name | GitHub |
|------|--------|
| Li Yongfu | [@yongfu-li](https://github.com/yongfu-li) |
| David MUY | [@Capeur](https://github.com/Capeur) |
| FanQin Zeng | [@FanqinZeng](https://github.com/FanqinZeng) |
| GateUltra | [@GateUltra](https://github.com/GateUltra) |
| muranfei | [@muranfei](https://github.com/muranfei) |
| stephQ-lab | [@stephQ-lab](https://github.com/stephQ-lab) |
| Supan | [@Su3037](https://github.com/Su3037) |
| thy031 | [@thy031](https://github.com/thy031) |
| xingguangyaoyu | [@xingguangyaoyu](https://github.com/xingguangyaoyu) |

## License

This work is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). See [`LICENSE`](LICENSE).

Siemens / Mentor Calibre documentation and tools are third-party products; their licenses are separate from this curriculum repository.

## Contact

- **Issues**: [github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language/issues](https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language/issues)
- **Organization**: [SJTU-YONGFU-RESEARCH-GRP](https://github.com/SJTU-YONGFU-RESEARCH-GRP)
- **Repository**: https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language
