# 09_growing_shopping_list.tcl — Week 3 Day 4: start small, lappend to grow
# Run: make week3-09
#      tclsh lessons/3/09_growing_shopping_list.tcl

set shopping [list milk bread]

puts "Trip start : $shopping"

lappend shopping apples
lappend shopping eggs
lappend shopping pencils

set n [llength $shopping]
puts "Trip end   : $shopping"
puts "Bought     : $n items total"
puts "First item : [lindex $shopping 0]"
puts "Last item  : [lindex $shopping end]"
