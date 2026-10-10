# 02_pet_two_objects.tcl — Week 6 Day 2: two objects from one class
# Run: make week6-02
#      tclsh lessons/6/02_pet_two_objects.tcl

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

set a [Pet new "Mimi" "cat"]
set b [Pet new "Buddy" "dog"]

puts "=== Pet A ==="
$a introduce
$a speak

puts "=== Pet B ==="
$b introduce
$b speak
