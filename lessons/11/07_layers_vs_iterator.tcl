# 07_layers_vs_iterator.tcl — Week 11 Day 4: layers list vs shape details
# Run: make week11-07
#      ./scripts/run_calibre_tcl.sh lessons/11/07_layers_vs_iterator.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week11_shapes.gds]
if {![file exists $gds]} {
    puts "Run make week11-01 first"
    exit 1
}

set L [layout create $gds]

puts "=== A) inventory (Week 9 style) ==="
puts "layers = [$L layers]"
puts "cells  = [$L cells]"

puts ""
puts "=== B) details (Week 11 iterator) ==="
foreach lyr [$L layers] {
    set polys [$L iterator poly TOP $lyr range 0 end]
    set wires [$L iterator wire TOP $lyr range 0 end]
    set texts [$L iterator text TOP $lyr range 0 end]
    puts "layer $lyr : poly=[llength $polys] wire=[llength $wires] text=[llength $texts]"
}

puts ""
puts "layers = which sheets exist"
puts "iterator = what drawings are on each sheet"
exit
