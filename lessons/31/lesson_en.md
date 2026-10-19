# Week 31 — Deep Hierarchy Query (Ancestors & Depth)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Query cell hierarchy relationships: ancestors, call depth (maxdepth), reference count (refcount), and topcell detection.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `ancestors` | `$L ancestors $cell` | List all parent cells instantiating this cell |
| `maxdepth` | `$L maxdepth $cell` | Get maximum hierarchy nesting depth |
| `refcount` | `$L refcount $cell` | Query reference instantiation count |
| `isReferenced` | `$L isReferenced $cell` | Check if cell is placed as instance inside another cell |
| `duplicate cell` | `$L duplicate cell $src $dst` | Deep clone a cell definition and contents |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 31 Example: Hierarchical Tree & Ancestor Traversal
set L [layout create]
$L create cell TOP
$L create cell MID
$L create cell LEAF
$L create ref MID LEAF 0 0 0 0 1
$L create ref TOP MID 0 0 0 0 1

puts "Ancestors of LEAF: [$L ancestors LEAF]"
puts "LEAF isReferenced: [$L isReferenced LEAF]"
puts "TOP max nesting depth: [$L maxdepth TOP]"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
