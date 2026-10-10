# 07_report_hierarchy.tcl — Week 24 Day 4: report after create ref
# Run: make week24-07
#      ./scripts/run_calibre_tcl.sh lessons/24/07_report_hierarchy.tcl
# Needs: tmp/week24_refs.gds (from week24-04) or creates a tiny one

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week24_refs.gds]

if {![file exists $gds]} {
    puts "(creating sample week24_refs.gds first)"
    set L0 [layout create]
    $L0 create cell BOX
    $L0 create layer 1
    $L0 create polygon BOX 1 0 0 20 20
    $L0 create cell TOP
    $L0 create ref TOP BOX 0 0 0 0 1
    $L0 create ref TOP BOX 40 0 0 0 1
    $L0 gdsout $gds TOP
}

puts "=== Hierarchy report ==="
puts "peek cells : [layout peek $gds -cells]"
puts "peek top   : [layout peek $gds -topcell]"

set L [layout create $gds -dt_expand]
puts "cells      : [$L cells]"
puts "topcell    : [$L topcell]"
puts "children   : [$L children [$L topcell]]"
puts "bbox TOP   : [$L bbox [$L topcell]]"
exit
