# 05_find_match.tcl — Week 6 Day 3: first / last / match / equal / compare
# Run: make week6-05

set s "banana"
puts "first 'a'  = [string first a $s]"
puts "last  'a'  = [string last a $s]"
puts "first 'z'  = [string first z $s]   ;# -1 means not found"
puts "match ban* = [string match ban* $s]"
puts "equal      = [string equal $s banana]"
puts "compare a b = [string compare a b]   ;# -1,0,1"
exit
