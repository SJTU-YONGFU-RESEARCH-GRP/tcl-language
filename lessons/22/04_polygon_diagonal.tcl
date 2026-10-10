# 04_polygon_diagonal.tcl — Week 22: rectangle with two opposite corners
# Run: make week22-04
#      ./scripts/run_calibre_tcl.sh lessons/22/04_polygon_diagonal.tcl
# Writes: tmp/week22_04_diag.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week22_04_diag.gds]

set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1

# Manual Script 1 style: two corners define a rectangle
$L create polygon TOP 1 0 0 100 100

puts "Diagonal-corner rectangle 0,0 -> 100,100"
$L gdsout $gds TOP
puts "Wrote $gds ([file size $gds] bytes)"
exit
