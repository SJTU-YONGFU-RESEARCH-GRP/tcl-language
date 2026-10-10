# 05_polygon_four_corners.tcl — Week 22: explicit four-corner polygon
# Run: make week22-05
#      ./scripts/run_calibre_tcl.sh lessons/22/05_polygon_four_corners.tcl
# Writes: tmp/week22_05_corners.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week22_05_corners.gds]

set L [layout create]
$L create cell TOP
$L create layer 1

# Same box as diagonal style, but list every corner
$L create polygon TOP 1_0 \
  0 0 \
  80 0 \
  80 60 \
  0 60

puts "Four-corner box 80x60"
$L gdsout $gds TOP
puts "Wrote $gds ([file size $gds] bytes)"
exit
