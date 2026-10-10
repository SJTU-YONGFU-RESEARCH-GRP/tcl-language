# 03_iterator_poly.tcl — Week 11 Day 1: list polygons on a layer
# Run: make week11-03
#      ./scripts/run_calibre_tcl.sh lessons/11/03_iterator_poly.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week11_shapes.gds]
if {![file exists $gds]} {
    puts "Run make week11-01 first"
    exit 1
}

set L [layout create $gds]
set polys [$L iterator poly TOP 1 range 0 end]

puts "=== iterator poly TOP layer 1 ==="
puts "count = [llength $polys]"
puts "raw   = $polys"
exit
