# 07_create_wire.tcl — Week 8 Day 4: create wire (path with width)
# Run: make week8-07
#      ./scripts/run_calibre_tcl.sh lessons/8/07_create_wire.tcl
# Writes: tmp/week8_07_wire.gds
#
# Usage: $L create wire cell L_D width x1 y1 x2 y2 ...

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week8_07_wire.gds]

set L [layout create]
$L create cell TOP
$L create layer 1
$L create layer 2

# A "path" on layer 2 with width 10, going right then up
$L create wire TOP 2_0 10 \
  0 0 \
  100 0 \
  100 50

puts "Wire width=10 along (0,0)->(100,0)->(100,50)"
$L gdsout $gds TOP
puts "Wrote $gds ([file size $gds] bytes)"
exit
