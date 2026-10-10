# 05_llength_count.tcl — Week 3 Day 3: count items with llength
# Run: make week3-05
#      tclsh lessons/3/05_llength_count.tcl

set fruits [list apple banana cherry orange grape]

set n [llength $fruits]

puts "Fruits : $fruits"
puts "Count  : $n"
puts "There are $n kinds of fruit on my list."
