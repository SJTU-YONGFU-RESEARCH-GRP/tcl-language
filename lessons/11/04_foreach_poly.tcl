# 04_foreach_poly.tcl — Week 11 Day 3: foreach over iterator results
# Run: make week11-04
#      ./scripts/run_calibre_tcl.sh lessons/11/04_foreach_poly.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week11_shapes.gds]
if {![file exists $gds]} {
    puts "Run make week11-01 first"
    exit 1
}

set L [layout create $gds]
set polys [$L iterator poly TOP 1 range 0 end]

puts "=== each polygon ==="
set n 0
foreach p $polys {
    incr n
    puts "$n) coords = $p"
}
puts "Total polygons: $n"
exit
