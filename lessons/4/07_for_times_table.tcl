# 07_for_times_table.tcl — Week 4 Day 3: for loop for a mini times table
# Run: make week4-07
#      tclsh lessons/4/07_for_times_table.tcl

set n 7

puts "=== Times table for $n ==="

for {set i 1} {$i <= 10} {incr i} {
    set product [expr {$n * $i}]
    puts "$n x $i = $product"
}
