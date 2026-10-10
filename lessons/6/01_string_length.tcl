# 01_string_length.tcl — Week 6 Day 1: string length
# Run: make week6-01
#      tclsh lessons/6/01_string_length.tcl

set s "Hello"
puts "s = \"$s\""
puts "string length = [string length $s]"
puts "empty length  = [string length {}]"
puts "Chinese tip: length counts characters in the Tcl string (encoding-aware)."
exit
