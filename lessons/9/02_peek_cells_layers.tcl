# 02_peek_cells_layers.tcl — Week 9 Day 1: layout peek without full load
# Run: make week9-02
#      ./scripts/run_calibre_tcl.sh lessons/9/02_peek_cells_layers.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week8_my_shapes.gds]
if {![file exists $gds]} {
    set gds [file join $repoRoot tmp week8_01_box.gds]
}
if {![file exists $gds]} {
    puts "ERROR: run make week8-10 first"
    exit 1
}

puts "=== layout peek (look through the window) ==="
puts "file   : $gds"
puts "cells  : [layout peek $gds -cells]"
puts "layers : [layout peek $gds -layers]"
puts "top    : [layout peek $gds -topcell]"
exit
