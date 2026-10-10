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

See the full collaborator list (avatars + table) in:

- [`CONTRIBUTORS.md`](CONTRIBUTORS.md) on this repository
- Course site: [Contributors](https://sjtu-yongfu-research-grp.github.io/tcl-language/contributors/) (GitHub Pages)

GitHub’s built-in **Insights → Contributors** graph only lists people who have made commits; it cannot show invited collaborators who have not committed yet.

## License

This work is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). See [`LICENSE`](LICENSE).

Siemens / Mentor Calibre documentation and tools are third-party products; their licenses are separate from this curriculum repository.

## Contact

- **Issues**: [github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language/issues](https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language/issues)
- **Organization**: [SJTU-YONGFU-RESEARCH-GRP](https://github.com/SJTU-YONGFU-RESEARCH-GRP)
- **Repository**: https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language
