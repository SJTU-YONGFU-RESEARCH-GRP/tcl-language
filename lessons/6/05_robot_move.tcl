# 05_robot_move.tcl — Week 6 Day 4: Robot move {steps} method
# Run: make week6-05
#      tclsh lessons/6/05_robot_move.tcl

oo::class create Robot {
    variable name steps

    constructor {n} {
        set name $n
        set steps 0
    }

    method beep {} {
        puts "$name: beep!"
    }

    method move {count} {
        set steps [expr {$steps + $count}]
        puts "$name moved $count step(s). Total steps: $steps"
    }

    method report {} {
        puts "$name has walked $steps steps in total."
    }
}

set bot [Robot new "Walker"]
$bot beep
$bot move 3
$bot move 2
$bot report
