# 09_simple_math.tcl — Week 2 Day 4: add and subtract with expr
# Run: make week2-09
#      tclsh lessons/2/09_simple_math.tcl

set apples 7
set eaten 2
set left [expr {$apples - $eaten}]

puts "Apples at start : $apples"
puts "Apples eaten    : $eaten"
puts "Apples left     : $left"

set a 15
set b 4
set sum [expr {$a + $b}]
set diff [expr {$a - $b}]

puts ""
puts "a + b = $sum"
puts "a - b = $diff"
