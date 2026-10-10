# 06_write_with_file_join.tcl — Week 5 Day 3: file join + write
# Run: make week5-06
#      tclsh lessons/5/06_write_with_file_join.tcl

file mkdir tmp

set dir tmp
set filename week5_notes.txt
set path [file join $dir $filename]

set fh [open $path w]
puts $fh "Line 1: file join builds a safe path."
puts $fh "Line 2: [file join a b c] works on any OS."
puts $fh "Line 3: Good night, Tcl."
close $fh

puts "Wrote notes to $path"
