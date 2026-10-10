# 05_create_ref_array.tcl — Week 10: array placement cols/rows
# Run: make week10-05
#      ./scripts/run_calibre_tcl.sh lessons/10/05_create_ref_array.tcl
# Writes: tmp/week10_05_array.gds
#
# Extra args: cols rows xspace yspace

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week10_05_array.gds]

set L [layout create]
$L units microns 1000

$L create cell DOT
$L create layer 1
$L create polygon DOT 1 0 0 8 8

$L create cell GRID
# 2 columns x 2 rows; spacing 15 in x and y
$L create ref GRID DOT 0 0 0 0 1 2 2 15 15

puts "GRID has 2x2 array of DOT"
puts "bbox GRID = [$L bbox GRID]"
$L gdsout $gds GRID
puts "Wrote $gds ([file size $gds] bytes)"
exit
