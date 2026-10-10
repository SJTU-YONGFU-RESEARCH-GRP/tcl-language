# 05_foreach_with_index.tcl — Week 4 Day 2: foreach + manual counter
# Run: make week4-05
#      tclsh lessons/4/05_foreach_with_index.tcl

set colors [list red green blue yellow]

set n 0
puts "=== Colors ==="
foreach color $colors {
    incr n
    puts "$n. $color"
}

puts "Total: $n colors"
