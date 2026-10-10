# 04_create_ref_two.tcl — Week 24: PLAN sample — two BOX refs + text
# Run: make week24-04
#      ./scripts/run_calibre_tcl.sh lessons/24/04_create_ref_two.tcl
# Writes: tmp/week24_refs.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week24_refs.gds]

set L [layout create]
$L units microns 1000
$L create cell BOX
$L create layer 1.0
$L create polygon BOX 1.0 0 0 20 20

$L create cell TOP
$L create ref TOP BOX 0 0 0 0 1
$L create ref TOP BOX 40 0 0 0 1
$L create text TOP 1.0 0 30 "TWO BOXES"

$L gdsout $gds TOP
puts "top=[$L topcell] cells=[$L cells]"
puts "Wrote $gds ([file size $gds] bytes)"
exit
