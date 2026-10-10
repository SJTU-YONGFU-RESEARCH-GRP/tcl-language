# 08_method_with_if.tcl — Week 6: method body uses if (from Week 4)
# Run: make week6-08
#      tclsh lessons/6/08_method_with_if.tcl

oo::class create Pet {
    variable name energy

    constructor {n e} {
        set name $n
        set energy $e
    }

    method mood {} {
        if {$energy >= 7} {
            puts "$name is happy and playful!"
        } elseif {$energy >= 4} {
            puts "$name is calm."
        } else {
            puts "$name is sleepy..."
        }
    }
}

set a [Pet new "Mimi" 8]
set b [Pet new "Buddy" 3]

$a mood
$b mood
