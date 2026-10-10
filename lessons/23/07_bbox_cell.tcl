# 07_bbox_cell.tcl — Week 23 Day 3: bounding box of a cell
# Run: make week23-07
#      ./scripts/run_calibre_tcl.sh lessons/23/07_bbox_cell.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week8_my_shapes.gds]
if {![file exists $gds]} {
    set gds [file join $repoRoot tmp week8_01_box.gds]
}
if {![file exists $gds]} {
    puts "ERROR: run make week8-10 first"
    exit 1
}

set L [layout create $gds]
set top [$L topcell]

if {[$L exists cell $top]} {
    set box [$L bbox $top]
    puts "topcell : $top"
    puts "bbox    : $box"
    puts "(bbox = left bottom right top — how big the room is)"
} else {
    puts "no topcell found"
}
exit
