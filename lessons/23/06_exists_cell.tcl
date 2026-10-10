# 06_exists_cell.tcl — Week 23 Day 3: exists cell + friendly if
# Run: make week23-06
#      ./scripts/run_calibre_tcl.sh lessons/23/06_exists_cell.tcl

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

foreach name {TOP CHIP SUB} {
    if {[$L exists cell $name]} {
        puts "cell $name : YES"
    } else {
        puts "cell $name : no"
    }
}
exit
