# 01_if_pass_fail.tcl — Week 4 Day 1: if score >= 60 then Pass else Fail
# Run: make week4-01
#      tclsh lessons/4/01_if_pass_fail.tcl

set score 75

if {$score >= 60} {
    puts "Pass"
} else {
    puts "Fail"
}

# Try a failing score too
set score 55
if {$score >= 60} {
    puts "Second test: Pass"
} else {
    puts "Second test: Fail"
}
