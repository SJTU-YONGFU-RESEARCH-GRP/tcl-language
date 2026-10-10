# 01_proc_greet.tcl — Week 5 Day 1: first proc greet
# Run: make week5-01
#      tclsh lessons/5/01_proc_greet.tcl

proc greet {name} {
    puts "Hi $name!"
}

greet "Amy"
greet "Bob"
greet "Tcl learner"
