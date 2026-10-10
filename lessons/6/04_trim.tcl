# 04_trim.tcl — Week 6 Day 2: trim family
# Run: make week6-04

set s "   padded   "
puts "raw      = <$s>"
puts "trim     = <[string trim $s]>"
puts "trimleft = <[string trimleft $s]>"
puts "trimright= <[string trimright $s]>"
puts "trim chars: [string trim xxhelloxx x]"
exit
