# 10_report_gds.tcl — Week 9 Day 5 project: GDS report script
# Run: make week9-10
#      ./scripts/run_calibre_tcl.sh lessons/9/10_report_gds.tcl
#      ./scripts/run_calibre_tcl.sh lessons/9/10_report_gds.tcl -- tmp/week8_01_box.gds
#
# Optional path after -- (calibredrv passes script args after --)

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]

set gds [lindex $argv 0]
if {$gds eq ""} {
    set gds [file join $repoRoot tmp week8_my_shapes.gds]
}
if {![file exists $gds]} {
    set gds [file join $repoRoot tmp week8_01_box.gds]
}
if {![file exists $gds]} {
    puts "ERROR: GDS not found. Run make week8-10, or pass a path after --"
    exit 1
}

puts "================================"
puts "         GDS REPORT"
puts "================================"
puts "file: $gds"
puts "size: [file size $gds] bytes"
puts "--------------------------------"
puts "PEEK (no full load)"
puts "  cells   : [layout peek $gds -cells]"
puts "  layers  : [layout peek $gds -layers]"
puts "  topcell : [layout peek $gds -topcell]"
puts "  precis. : [layout peek $gds -precision]"
puts "--------------------------------"
puts "LOADED layout create"
set L [layout create $gds -dt_expand]
puts "  handle  : $L"
puts "  file    : [$L file]"
puts "  topcell : [$L topcell]"
puts "  cells   : [$L cells]"
puts "  layers  : [$L layers]"

set top [$L topcell]
if {[$L exists cell $top]} {
    puts "  bbox $top : [$L bbox $top]"
} else {
    puts "  (no topcell bbox)"
}
puts "================================"
exit
