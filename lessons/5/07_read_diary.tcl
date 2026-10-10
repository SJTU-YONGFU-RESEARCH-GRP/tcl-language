# 07_read_diary.tcl — Week 5 Day 4: read a file and print lines
# Run: make week5-07
#      tclsh lessons/5/07_read_diary.tcl
# Reads tmp/week5_diary.txt (creates sample if missing)

file mkdir tmp

set path tmp/week5_diary.txt

if {![file exists $path]} {
    set fh [open $path w]
    puts $fh "Sample line 1"
    puts $fh "Sample line 2"
    close $fh
    puts "(Created sample $path first)"
}

set fh [open $path r]
puts "=== Contents of $path ==="

while {[gets $fh line] >= 0} {
    puts $line
}

close $fh
puts "=== End of file ==="
