# 03_if_check_three_scores.tcl — Week 4 Day 1: if each subject score
# Run: make week4-03
#      tclsh lessons/4/03_if_check_three_scores.tcl

set math 88
set english 72
set science 59

puts "=== Score check (pass if >= 60) ==="

if {$math >= 60} {
    puts "Math    : Pass ($math)"
} else {
    puts "Math    : Fail ($math)"
}

if {$english >= 60} {
    puts "English : Pass ($english)"
} else {
    puts "English : Fail ($english)"
}

if {$science >= 60} {
    puts "Science : Pass ($science)"
} else {
    puts "Science : Fail ($science)"
}
