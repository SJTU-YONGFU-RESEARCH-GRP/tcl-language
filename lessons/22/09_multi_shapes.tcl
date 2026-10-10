# 09_multi_shapes.tcl — Week 22: polygon + wire + text together
# Run: make week22-09
#      ./scripts/run_calibre_tcl.sh lessons/22/09_multi_shapes.tcl
# Writes: tmp/week22_09_multi.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week22_09_multi.gds]

set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1.0
$L create layer 2.0

$L create polygon TOP 1.0 0 0 100 100
$L create wire TOP 2.0 8 0 50  50 50  100 50
$L create text TOP 1.0 10 110 MULTI

puts "polygon + wire + text on TOP"
$L gdsout $gds TOP
puts "Wrote $gds ([file size $gds] bytes)"
exit
