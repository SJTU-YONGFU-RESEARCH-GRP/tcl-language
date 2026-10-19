> **Student Submission — GateUltra**
>
> VLSI Tcl Language Homework, Weeks 1–6 — **6/6 PASS**
>
> [View my homework and validation results](homework/README.md)


# VLSI Tcl Language Homework

- Student / GitHub name: **GateUltra**
- School: Shanghai Jiao Tong University
- Course context: VLSI Design
- Completed scope: **Week 1–6**
- Tested environment: **Tcl 8.6.18**, standard `tclsh`

| Week | Topic | Submission | Status |
| --- | --- | --- | --- |
| 1 | `puts` and comments | [Self-introduction card](week01/self_intro_card.tcl) | PASS |
| 2 | Variables, substitution, quoting, `expr` | [Example report card](week02/report_card.tcl) | PASS |
| 3 | Lists and zero-based indexing | [Study schedule](week03/today_schedule.tcl) | PASS |
| 4 | Conditions and loops | [Batch guess-number game](week04/guess_number_game.tcl) | PASS |
| 5 | Procedures and file I/O | [Toolbox](week05/toolbox.tcl) | PASS |
| 6 | String processing and `slugify` | [String toolkit](week06/string_toolkit.tcl) | PASS |

Run from the repository root:

```powershell
tclsh homework/week01/self_intro_card.tcl
tclsh homework/week02/report_card.tcl
tclsh homework/week03/today_schedule.tcl
tclsh homework/week04/guess_number_game.tcl
tclsh homework/week05/toolbox.tcl
tclsh homework/week06/string_toolkit.tcl
```

[reports/runs/](../reports/runs/) contains actual execution output for all six
scripts. Weeks 5 and 6 save and read back files in their own `output/` directories,
located relative to the script. Scores and schedules are example data.

## Source

`lessons/`, `PLAN.md`, and other teaching materials come from
[SJTU-YONGFU-RESEARCH-GRP/tcl-language](https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language).
`homework/` and `reports/` are the personal coursework completed here, with
VLSI-related examples and separate output files. Original teaching files are unchanged.

Teaching source: Copyright (c) 2026 SJTU-YONGFU-RESEARCH-GRP,
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see [LICENSE](../LICENSE).
