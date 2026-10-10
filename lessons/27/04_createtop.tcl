# 04_createtop.tcl — Week 27 Day 3: -createtop wrapper cell
# Run: make week27-04
#      ./scripts/run_calibre_tcl.sh lessons/27/04_createtop.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
set left  [file join $outDir week27_left.gds]
set right [file join $outDir week27_right.gds]
set out   [file join $outDir week27_createtop.gds]

proc ensure {path cell x0 y0 x1 y1} {
    if {[file exists $path]} { return }
    set L [layout create]
    $L units microns 1000
    $L create cell $cell
    $L create layer 1
    $L create polygon $cell 1_0 $x0 $y0 $x1 $y1
    $L gdsout $path $cell
}
ensure $left LEFT 0 0 10 10
ensure $right RIGHT 0 0 8 8

file delete -force $out
layout filemerge -in $left -in $right -out $out -createtop CHIP

set M [layout create $out -dt_expand]
puts "cells = [$M cells]"
puts "children CHIP = [$M children CHIP]"
puts "refs CHIP = [$M iterator ref CHIP range 0 end]"
puts "Expected: CHIP with children LEFT and RIGHT"
exit
