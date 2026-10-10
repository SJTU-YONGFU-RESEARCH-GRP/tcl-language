# 05_topcell_cells_layers.tcl — Week 23 Day 2: ask the layout questions
# Run: make week23-05
#      ./scripts/run_calibre_tcl.sh lessons/23/05_topcell_cells_layers.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week8_my_shapes.gds]
if {![file exists $gds]} {
    set gds [file join $repoRoot tmp week8_01_box.gds]
}
if {![file exists $gds]} {
    puts "ERROR: run make week8-10 first"
    exit 1
}

set L [layout create $gds -dt_expand]

puts "=== Ask the layout ==="
puts "topcell : [$L topcell]"
puts "cells   : [$L cells]"
puts "layers  : [$L layers]"
exit
