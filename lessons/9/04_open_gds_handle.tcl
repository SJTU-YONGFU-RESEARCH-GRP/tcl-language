# 04_open_gds_handle.tcl — Week 9 Day 2: layout create $gds -> handle
# Run: make week9-04
#      ./scripts/run_calibre_tcl.sh lessons/9/04_open_gds_handle.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week8_my_shapes.gds]
if {![file exists $gds]} {
    set gds [file join $repoRoot tmp week8_01_box.gds]
}
if {![file exists $gds]} {
    puts "ERROR: run make week8-10 first"
    exit 1
}

puts "Opening (full load): $gds"
set L [layout create $gds]
puts "Handle L = $L"
puts "This is like Week 7, but the paper already has drawings."
exit
