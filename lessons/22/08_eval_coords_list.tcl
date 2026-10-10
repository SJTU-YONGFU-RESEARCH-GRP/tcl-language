# 08_eval_coords_list.tcl — Week 22 Day 4: expand a coord list with eval
# Run: make week22-08
#      ./scripts/run_calibre_tcl.sh lessons/22/08_eval_coords_list.tcl
# Writes: tmp/week22_08_eval.gds
#
# create polygon wants flat numbers. If coords are in a list, use eval.

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week22_08_eval.gds]

set L [layout create]
$L create cell TOP
$L create layer 1

set coords {0 0 40 0 40 30 0 30}
# WRONG (do not do this):  $L create polygon TOP 1 $coords
# RIGHT:
eval $L create polygon TOP 1 $coords

puts "Used eval to expand coords list: $coords"
$L gdsout $gds TOP
puts "Wrote $gds ([file size $gds] bytes)"
exit
