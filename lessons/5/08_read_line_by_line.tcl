# 08_read_line_by_line.tcl — Week 5 Day 4: gets in a while loop
# Run: make week5-08
#      tclsh lessons/5/08_read_line_by_line.tcl

file mkdir tmp

set path tmp/week5_notes.txt

if {![file exists $path]} {
    set fh [open $path w]
    puts $fh "Note A"
    puts $fh "Note B"
    puts $fh "Note C"
    close $fh
}

set fh [open $path r]
set n 0

puts "=== Reading $path ==="
while {[gets $fh line] >= 0} {
    incr n
    puts "$n) $line"
}

close $fh
puts "Read $n lines."
