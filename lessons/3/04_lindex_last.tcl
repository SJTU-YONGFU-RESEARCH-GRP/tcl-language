# 04_lindex_last.tcl — Week 3 Day 2: first, second, and last item
# Run: make week3-04
#      tclsh lessons/3/04_lindex_last.tcl

set fruits [list apple banana cherry orange]

set first [lindex $fruits 0]
set second [lindex $fruits 1]

# Two ways to get the last item:
# 1) lindex with the word "end" (easy)
set last [lindex $fruits end]

# 2) llength minus 1 (good to understand counting)
set count [llength $fruits]
set lastIndex [expr {$count - 1}]
set lastByMath [lindex $fruits $lastIndex]

puts "List        : $fruits"
puts "First (0)   : $first"
puts "Second (1)  : $second"
puts "Last (end)  : $last"
puts "Last (math) : $lastByMath"
