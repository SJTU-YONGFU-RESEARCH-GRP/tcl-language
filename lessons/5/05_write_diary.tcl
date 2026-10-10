# 05_write_diary.tcl — Week 5 Day 3: write lines to a text file
# Run: make week5-05
#      tclsh lessons/5/05_write_diary.tcl
# Creates: tmp/week5_diary.txt (from project root)

file mkdir tmp

set path tmp/week5_diary.txt
set fh [open $path w]

puts $fh "=== My Tcl Diary ==="
puts $fh "Today I learned proc and files."
puts $fh "I can write text to tmp/week5_diary.txt"
puts $fh "Tomorrow I will read it back."

close $fh

puts "Wrote diary to $path"
