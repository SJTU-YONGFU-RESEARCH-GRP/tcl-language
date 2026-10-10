# 03_filemerge_basic.tcl — Week 27 Day 2: basic -in/-in/-out merge
# Run: make week27-03
#      ./scripts/run_calibre_tcl.sh lessons/27/03_filemerge_basic.tcl
# Needs: make week27-01 first (or we rebuild inputs)

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set left  [file join $outDir week27_left.gds]
set right [file join $outDir week27_right.gds]
set merged [file join $outDir week27_merged.gds]

# Ensure inputs exist
proc ensure {path cell x0 y0 x1 y1} {
    if {[file exists $path]} { return }
    set L [layout create]
    $L units microns 1000
    $L create cell $cell
    $L create layer 1
    $L create polygon $cell 1_0 $x0 $y0 $x1 $y1
    $L gdsout $path $cell
}
ensure $left  LEFT  0 0 10 10
ensure $right RIGHT 0 0 8 8

file delete -force $merged
layout filemerge -in $left -in $right -out $merged

set M [layout create $merged -dt_expand]
puts "Merged file: $merged"
puts "cells = [$M cells]"
foreach c [$M cells] {
    puts "  $c  npoly=[llength [$M iterator poly $c 1 range 0 end]]"
}
puts "Expected: LEFT and RIGHT both present."
exit
