# 03_lindex_first.tcl — Week 3 Day 2: lindex picks one item (index 0 = first)
# Run: make week3-03
#      tclsh lessons/3/03_lindex_first.tcl

set colors [list red green blue yellow]

# Index counting starts at 0!
# 0 = first, 1 = second, 2 = third ...
set first [lindex $colors 0]
set second [lindex $colors 1]

puts "The whole list : $colors"
puts "First color    : $first   (index 0)"
puts "Second color   : $second  (index 1)"
