# 06_lappend_add.tcl — Week 3 Day 4: add items with lappend
# Run: make week3-06
#      tclsh lessons/3/06_lappend_add.tcl

set fruits [list apple banana cherry]

puts "Before: $fruits (count [llength $fruits])"

# lappend adds one new item to the end of the list in the variable
lappend fruits orange
lappend fruits grape

puts "After : $fruits (count [llength $fruits])"
