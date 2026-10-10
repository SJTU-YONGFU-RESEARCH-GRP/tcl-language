# 02_if_else_messages.tcl — Week 4 Day 1: if / else with friendly messages
# Run: make week4-02
#      tclsh lessons/4/02_if_else_messages.tcl

set score 88

if {$score >= 90} {
    puts "Excellent! Score: $score"
} elseif {$score >= 60} {
    puts "Good job. Score: $score"
} else {
    puts "Keep practicing. Score: $score"
}

set score 52
if {$score >= 60} {
    puts "Result: Pass ($score)"
} else {
    puts "Result: Fail ($score)"
}
