# 11_compare_two_gds.tcl — Week 9 bonus: peek two GDS files side by side
# Run: make week9-11
#      ./scripts/run_calibre_tcl.sh lessons/9/11_compare_two_gds.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set a [file join $repoRoot tmp week8_01_box.gds]
set b [file join $repoRoot tmp week8_my_shapes.gds]
if {![file exists $a]} {
    set a [file join $repoRoot tmp demo_box.gds]
}
if {![file exists $b]} {
    set b $a
}

proc showPeek {label gds} {
    puts "--- $label ---"
    puts "file   : $gds"
    if {![file exists $gds]} {
        puts "MISSING"
        return
    }
    puts "cells  : [layout peek $gds -cells]"
    puts "layers : [layout peek $gds -layers]"
    puts "top    : [layout peek $gds -topcell]"
}

showPeek "A" $a
puts ""
showPeek "B" $b
exit
