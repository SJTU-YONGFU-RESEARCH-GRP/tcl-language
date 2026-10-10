# 04_robot_basic.tcl — Week 6 Day 4: Robot class with beep
# Run: make week6-04
#      tclsh lessons/6/04_robot_basic.tcl

oo::class create Robot {
    variable name

    constructor {n} {
        set name $n
    }

    method introduce {} {
        puts "Robot online: $name"
    }

    method beep {} {
        puts "$name: beep beep!"
    }
}

set r1 [Robot new "R2"]
$r1 introduce
$r1 beep

set r2 [Robot new "Helper"]
$r2 introduce
$r2 beep
