# 02_store_and_print_list.tcl — Week 3 Day 1: store list, print each part
# Run: make week3-02
#      tclsh lessons/3/02_store_and_print_list.tcl

set fruits [list apple banana cherry orange grape]

puts "=== Fruit shopping list ==="
puts "Raw list : $fruits"
puts "Item 1   : [lindex $fruits 0]"
puts "Item 2   : [lindex $fruits 1]"
puts "Item 3   : [lindex $fruits 2]"
