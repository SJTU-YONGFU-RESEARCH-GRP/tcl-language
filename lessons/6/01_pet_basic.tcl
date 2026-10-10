# 01_pet_basic.tcl — Week 6 Day 2: first TclOO Pet class
# Run: make week6-01
#      tclsh lessons/6/01_pet_basic.tcl

oo::class create Pet {
    variable name kind

    constructor {n k} {
        set name $n
        set kind $k
    }

    method introduce {} {
        puts "I am $name, a $kind."
    }

    method speak {} {
        if {$kind eq "cat"} {
            puts "$name: meow!"
        } else {
            puts "$name: woof!"
        }
    }
}

set cat [Pet new "Mimi" "cat"]
$cat introduce
$cat speak
