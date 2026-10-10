# 08_count_all_shapes.tcl — Week 25: count poly+wire+text on all layers
# Run: make week25-08
#      ./scripts/run_calibre_tcl.sh lessons/25/08_count_all_shapes.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week25_shapes.gds]
if {![file exists $gds]} {
    puts "Run make week25-01 first"
    exit 1
}

set L [layout create $gds]
set top [$L topcell]

set nPoly 0
set nWire 0
set nText 0
foreach lyr [$L layers] {
    incr nPoly [llength [$L iterator poly $top $lyr range 0 end]]
    incr nWire [llength [$L iterator wire $top $lyr range 0 end]]
    incr nText [llength [$L iterator text $top $lyr range 0 end]]
}

puts "Shape census for cell $top"
puts "  polygons : $nPoly"
puts "  wires    : $nWire"
puts "  texts    : $nText"
puts "  TOTAL    : [expr {$nPoly + $nWire + $nText}]"
exit
