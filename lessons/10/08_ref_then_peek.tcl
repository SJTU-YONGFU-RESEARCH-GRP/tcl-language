# 08_ref_then_peek.tcl — Week 10: build, save, peek in one script
# Run: make week10-08
#      ./scripts/run_calibre_tcl.sh lessons/10/08_ref_then_peek.tcl
# Writes: tmp/week10_08_roundtrip.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week10_08_roundtrip.gds]

set L [layout create]
$L create cell TILE
$L create layer 1
$L create polygon TILE 1 0 0 10 10
$L create cell TOP
$L create ref TOP TILE 0 0 0 0 1
$L create ref TOP TILE 20 0 0 0 1
$L create ref TOP TILE 40 0 0 0 1
$L gdsout $gds TOP

puts "Created 3 TILE refs"
puts "peek cells=[layout peek $gds -cells] top=[layout peek $gds -topcell]"
exit
