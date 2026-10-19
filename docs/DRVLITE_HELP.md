# DRV-Lite: Pure-Tcl Calibre DESIGNrev Simulator Guide

[English](DRVLITE_HELP.md) · [Home](../index.md) · [Timing Lab](TIMING_ANALYZER_LAB.md)

---

## 1. Problem Statement & Motivation

In Weeks 21 through 40 of this curriculum, students advance from general Tcl programming to IC layout scripting using Siemens **Calibre DESIGNrev** (`calibredrv`). 

However, commercial EDA tools present major accessibility barriers:
- **Proprietary Licenses**: `calibredrv` requires expensive FlexNet / Mentor Graphics license daemons.
- **Environment Barriers**: Commercial EDA tools typically run only on RedHat / Rocky Linux enterprise servers, making local study on macOS or Windows laptops impossible.
- **Batch Evaluation**: Automated grading in CI/CD pipelines (e.g. GitHub Actions) cannot run commercial license daemons.

**DRV-Lite** solves this by providing a lightweight, pure-Tcl implementation of Calibre DESIGNrev's `layout` object model. Any standard `tclsh` (Tcl 8.5/8.6/9.0) can execute layout manipulation scripts without external dependencies.

---

## 2. Supported API Surface

DRV-Lite implements the core methods of Calibre DESIGNrev's `layout` handle:

| Command / Method | Description | Return Value / Effect |
| :--- | :--- | :--- |
| `layout create ?file?` | Instantiate an in-memory layout object handle | Layout handle (e.g., `::drvlite::layout0`) |
| `layout peek <file> -topcell` | Inspect topcell of an existing GDS file | Top cell name |
| `$L create cell <name>` | Create a new hierarchical cell | Cell name |
| `$L create layer <num>` | Register a layout layer | Layer number |
| `$L create polygon <cell> <layer> <x1> <y1> ...` | Create an arbitrary polygonal boundary | Polygon record |
| `$L create wire <cell> <layer> <width> <x1> <y1> ...` | Create a routing path / wire with width | Wire record |
| `$L create text <cell> <layer> <x> <y> <text>` | Add text label to a cell | Text record |
| `$L create ref <parent> <child> <x> <y> ?orient?` | Instantiate cell reference / hierarchy | Reference record |
| `$L bbox <cell>` | Compute bounding box `[xmin ymin xmax ymax]` | 4-element list of coordinates |
| `$L topcell` | Get or detect topcell name | Top cell name |
| `$L cells` | List all cell names in layout | List of strings |
| `$L layers ?cell?` | List all layers used in layout or cell | List of layer numbers |
| `$L exists cell <name>` | Check if cell exists | `1` or `0` |
| `$L exists layer <cell> <layer>` | Check if layer has shapes in cell | `1` or `0` |
| `$L gdsout <file> ?topcell?` | Export layout to GDS-II stream | Creates `.gds` file |
| `$L oasisout <file> ?topcell?` | Export layout to OASIS stream | Creates `.oasis` file |
| `$L delete cell <name>` | Delete a cell and its contents | Empty |

---

## 3. Architecture & Mental Model

```
+-------------------------------------------------------+
|              Tcl Script (Weeks 21-40)                 |
|   set L [layout create]                               |
|   $L create cell INV_X1                               |
|   $L create polygon INV_X1 1 0 0 100 0 100 200 0 200  |
+-------------------------------------------------------+
                           |
       +-------------------+-------------------+
       |                                       |
  [calibredrv] (Commercial EDA)          [DRV-Lite] (Pure Tcl)
  - Requires FlexNet License             - Zero external dependencies
  - Runs in enterprise Linux             - Runs in standard tclsh 8.6
  - Full GDS/OASIS renderer              - In-memory hierarchical model
                                         - Automated test runner & CI
```

---

## 4. Usage Example

```tcl
#!/usr/bin/env tclsh
# Load DRV-Lite simulator
source [file join [file dirname [info script]] ".." "tools" "drvlite" "drvlite.tcl"]

# 1. Create layout object
set L [layout create]

# 2. Build cell hierarchy
$L create cell TOP
$L create cell NAND2

# 3. Add geometry to NAND2
$L create polygon NAND2 1 0 0 200 0 200 150 0 150
$L create wire NAND2 2 10 50 20 150 20

# 4. Instantiate NAND2 in TOP
$L create ref TOP NAND2 0 0 R0
$L create ref TOP NAND2 250 0 R0

# 5. Query layout bounds
set bounds [$L bbox TOP]
puts "TOP bounding box: $bounds"
# Output: TOP bounding box: 0 0 450 150

# 6. Stream out
$L gdsout "chip_top.gds"
puts "Successfully exported layout to chip_top.gds"
```

---

## 5. Automated Verification

Run DRV-Lite unit self-tests directly from repo root:

```bash
make drvlite-test
```

Or run Week 21 layout script with DRV-Lite simulation:

```bash
make week21-01
```
