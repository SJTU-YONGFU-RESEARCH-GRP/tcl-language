# 09_word_byte.tcl — Week 6 bonus: wordstart / wordend / bytelength
# Run: make week6-09

set s "hello world"
puts "wordstart at 7 = [string wordstart $s 7]"
puts "wordend   at 7 = [string wordend $s 7]"
puts "length      = [string length $s]"
puts "bytelength  = [string bytelength $s]"
exit
