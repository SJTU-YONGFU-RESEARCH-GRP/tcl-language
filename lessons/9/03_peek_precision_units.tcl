# 03_peek_precision_units.tcl — Week 9: peek precision and units
# Run: make week9-03
#      ./scripts/run_calibre_tcl.sh lessons/9/03_peek_precision_units.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week8_my_shapes.gds]
if {![file exists $gds]} {
    set gds [file join $repoRoot tmp week8_01_box.gds]
}
if {![file exists $gds]} {
    puts "ERROR: run make week8-10 first"
    exit 1
}

puts "=== peek ruler info ==="
puts "precision : [layout peek $gds -precision]"
puts "units     : [layout peek $gds -units]"
puts "(precision / units describe how fine the drawing grid is)"
exit
