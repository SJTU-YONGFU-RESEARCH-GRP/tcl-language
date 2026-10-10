# 01_create_box_like.tcl — Week 22 Day 1: box like examples/create_box.tcl
# Run: make week22-01
#      ./scripts/run_calibre_tcl.sh lessons/22/01_create_box_like.tcl
# Writes: tmp/week22_01_box.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set gds [file join $outDir week22_01_box.gds]

set L [layout create]
$L create cell TOP
$L create layer 1

# Four corners of a 100x100 box; L_D style 1_0 = layer 1 datatype 0
$L create polygon TOP 1_0 \
  0 0 \
  100 0 \
  100 100 \
  0 100

puts "Writing $gds"
$L gdsout $gds TOP
puts "done size=[file size $gds] bytes"
exit
