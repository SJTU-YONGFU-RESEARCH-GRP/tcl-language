# 02_leaf_cell_box.tcl — Week 24: leaf cell BOX with one polygon
# Run: make week24-02
#      ./scripts/run_calibre_tcl.sh lessons/24/02_leaf_cell_box.tcl
# Writes: tmp/week24_02_box.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week24_02_box.gds]

set L [layout create]
$L units microns 1000
$L create cell BOX
$L create layer 1.0
$L create polygon BOX 1.0 0 0 20 20

puts "Leaf cell BOX = 20x20 square"
$L gdsout $gds BOX
puts "Wrote $gds ([file size $gds] bytes)"
exit
