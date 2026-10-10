# 07_print_each_manual.tcl — Week 3: print every item using lindex
# Run: make week3-07
#      tclsh lessons/3/07_print_each_manual.tcl
# Note: Week 4 will teach foreach — for now we use lindex by hand.

set pets [list cat dog rabbit hamster]

set n [llength $pets]

puts "=== My pets ($n total) ==="
puts "1. [lindex $pets 0]"
puts "2. [lindex $pets 1]"
puts "3. [lindex $pets 2]"
puts "4. [lindex $pets 3]"
