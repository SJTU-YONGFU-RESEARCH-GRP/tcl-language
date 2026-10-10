# 08_layout_create_from_gds.tcl — Week 7: open layout from GDS file
# Run: make week7-08
#      ./scripts/run_calibre_tcl.sh lessons/7/08_layout_create_from_gds.tcl
#
# Uses tmp/week7_script1.gds if present, else tmp/demo_box.gds.
# Run make week7-07 or examples/create_box.tcl first if neither exists.

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds1 [file join $repoRoot tmp week7_script1.gds]
set gds2 [file join $repoRoot tmp demo_box.gds]

if {[file exists $gds1]} {
    set gds $gds1
} elseif {[file exists $gds2]} {
    set gds $gds2
} else {
    puts "No GDS found. Run make week7-07 first."
    exit 1
}

puts "Opening GDS: $gds"
set L [layout create $gds]
puts "Layout handle from file: $L"

exit
