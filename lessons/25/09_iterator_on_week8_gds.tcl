# 09_iterator_on_week8_gds.tcl — Week 25: iterate a previous homework GDS
# Run: make week25-09
#      ./scripts/run_calibre_tcl.sh lessons/25/09_iterator_on_week8_gds.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week8_my_shapes.gds]
if {![file exists $gds]} {
    set gds [file join $repoRoot tmp week8_01_box.gds]
}
if {![file exists $gds]} {
    set gds [file join $repoRoot tmp week25_shapes.gds]
}
if {![file exists $gds]} {
    puts "ERROR: no GDS found. Run make week25-01 or week8-10"
    exit 1
}

set L [layout create $gds]
set top [$L topcell]
puts "file=$gds top=$top layers=[$L layers]"

foreach lyr [$L layers] {
    set n [llength [$L iterator poly $top $lyr range 0 end]]
    puts "layer $lyr polygons: $n"
}
exit
