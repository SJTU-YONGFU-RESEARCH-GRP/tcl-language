# 08_fruit_count_message.tcl — Week 3 Day 3: full count message
# Run: make week3-08
#      tclsh lessons/3/08_fruit_count_message.tcl

set fruits [list apple banana cherry mango pineapple]

set n [llength $fruits]
set firstFruit [lindex $fruits 0]
set lastFruit [lindex $fruits end]

puts "================================"
puts "       FRUIT INVENTORY"
puts "================================"
puts "List   : $fruits"
puts "Count  : $n kinds of fruit"
puts "First  : $firstFruit"
puts "Last   : $lastFruit"
puts "================================"
