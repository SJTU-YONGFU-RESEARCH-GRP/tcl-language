# 06_map_replace.tcl — Week 6 Day 4: map / replace
# Run: make week6-06

set s "I like cats and cats"
puts "map:    [string map {cats dogs like love} $s]"
puts "replace index 2-3 with XX: [string replace $s 2 3 XX]"
puts "replace delete 2-3:        [string replace $s 2 3]"
exit
