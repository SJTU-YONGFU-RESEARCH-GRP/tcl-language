# 05_mode_rename.tcl — Week 27 Day 3: same cell name → -mode rename
# Run: make week27-05
#      ./scripts/run_calibre_tcl.sh lessons/27/05_mode_rename.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir

proc write_top {path ox} {
    set L [layout create]
    $L units microns 1000
    $L create cell TOP
    $L create layer 1
    $L create polygon TOP 1_0 $ox 0 [expr {$ox + 10}] 10
    $L gdsout $path TOP
}

set t1 [file join $outDir week27_same_a.gds]
set t2 [file join $outDir week27_same_b.gds]
set out [file join $outDir week27_renamed.gds]
write_top $t1 0
write_top $t2 20

file delete -force $out
# Use -mode rename only (do NOT also pass -overwrite flag)
layout filemerge -in $t1 -in $t2 -out $out -mode rename

set M [layout create $out -dt_expand]
puts "cells after -mode rename = [$M cells]"
puts "Tip: one stays TOP; the other often becomes TOP_WB1 (or similar)."
exit
