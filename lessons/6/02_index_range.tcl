# 02_index_range.tcl — Week 6 Day 1: string index / range
# Run: make week6-02

set s "ABCDEF"
puts "s = $s"
puts "index 0   = [string index $s 0]"
puts "index end = [string index $s end]"
puts "range 1 3 = [string range $s 1 3]"
puts "range 2 end = [string range $s 2 end]"
exit
