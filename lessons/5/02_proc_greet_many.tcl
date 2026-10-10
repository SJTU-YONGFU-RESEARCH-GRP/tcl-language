# 02_proc_greet_many.tcl — Week 5 Day 1: proc + foreach together
# Run: make week5-02
#      tclsh lessons/5/02_proc_greet_many.tcl

proc greet {name} {
    puts "Welcome, $name!"
}

set friends [list Amy Bob Mimi]

foreach person $friends {
    greet $person
}
