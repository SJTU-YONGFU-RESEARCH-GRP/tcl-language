# 03_pet_rename.tcl — Week 15 Day 3: add rename method
# Run: make week15-03
#      tclsh lessons/15/03_pet_rename.tcl

oo::class create Pet {
    variable name kind

    constructor {n k} {
        set name $n
        set kind $k
    }

    method introduce {} {
        puts "I am $name, a $kind."
    }

    method rename {newName} {
        set name $newName
        puts "(Name changed to $name)"
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

$cat rename "Snowball"
$cat introduce
$cat speak
