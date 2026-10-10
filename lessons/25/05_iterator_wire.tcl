# 05_iterator_wire.tcl — Week 25 Day 2: iterate wires
# Run: make week25-05
#      ./scripts/run_calibre_tcl.sh lessons/25/05_iterator_wire.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week25_shapes.gds]
if {![file exists $gds]} {
    puts "Run make week25-01 first"
    exit 1
}

set L [layout create $gds]
set wires [$L iterator wire TOP 2 range 0 end]

puts "=== iterator wire TOP layer 2 ==="
puts "count = [llength $wires]"
set n 0
foreach w $wires {
    incr n
    puts "$n) $w"
}
exit
