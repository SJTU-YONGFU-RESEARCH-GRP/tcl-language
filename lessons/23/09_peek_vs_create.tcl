# 09_peek_vs_create.tcl — Week 23 Day 4: peek vs full layout create
# Run: make week23-09
#      ./scripts/run_calibre_tcl.sh lessons/23/09_peek_vs_create.tcl

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set gds [file join $repoRoot tmp week8_my_shapes.gds]
if {![file exists $gds]} {
    set gds [file join $repoRoot tmp week8_01_box.gds]
}
if {![file exists $gds]} {
    puts "ERROR: run make week8-10 first"
    exit 1
}

puts "=== A) layout peek (fast look, no full object) ==="
puts "peek cells  : [layout peek $gds -cells]"
puts "peek layers : [layout peek $gds -layers]"
puts "peek top    : [layout peek $gds -topcell]"

puts ""
puts "=== B) layout create (full load -> handle \$L) ==="
set L [layout create $gds -dt_expand]
puts "handle      : $L"
puts "\$L cells    : [$L cells]"
puts "\$L layers   : [$L layers]"
puts "\$L topcell  : [$L topcell]"
puts "\$L bbox     : [$L bbox [$L topcell]]"

puts ""
puts "Difference: peek answers quick questions;"
puts "            create gives a handle for more methods (bbox, exists, ...)."
exit
