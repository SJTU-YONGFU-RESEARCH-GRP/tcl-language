# 01_build_two_gds.tcl — Week 27 Day 1: two small GDS inputs
# Run: make week27-01
#      ./scripts/run_calibre_tcl.sh lessons/27/01_build_two_gds.tcl
# Writes: tmp/week27_left.gds , tmp/week27_right.gds

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir

proc write_block {path cell x0 y0 x1 y1} {
    set L [layout create]
    $L units microns 1000
    $L create cell $cell
    $L create layer 1
    $L create polygon $cell 1_0 $x0 $y0 $x1 $y1
    $L gdsout $path $cell
    puts "Wrote $path  cell=$cell  box=($x0,$y0)-($x1,$y1)"
}

set left  [file join $outDir week27_left.gds]
set right [file join $outDir week27_right.gds]
write_block $left  LEFT  0 0 10 10
write_block $right RIGHT 0 0 8 8
puts "Day 1 done — two inputs ready for filemerge."
exit
