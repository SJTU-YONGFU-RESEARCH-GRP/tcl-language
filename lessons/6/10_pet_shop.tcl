# 10_pet_shop.tcl — Week 6 Day 5 project: pet shop
# Run: make week6-10
#      tclsh lessons/6/10_pet_shop.tcl
# Optional: copy to examples/my_oop_pets.tcl and customize.

oo::class create Pet {
    variable name kind age

    constructor {n k a} {
        set name $n
        set kind $k
        set age $a
    }

    method introduce {} {
        puts "  $name — a $kind, age $age"
    }

    method speak {} {
        if {$kind eq "cat"} {
            puts "  $name: meow!"
        } else {
            puts "  $name: woof!"
        }
    }

    method birthday {} {
        incr age
        puts "  Happy birthday $name! Now age $age."
    }
}

puts "================================"
puts "         PET SHOP"
puts "================================"

set p1 [Pet new "Mimi" "cat" 2]
set p2 [Pet new "Buddy" "dog" 4]
set p3 [Pet new "Snowball" "cat" 1]

puts "For sale today:"
$p1 introduce
$p2 introduce
$p3 introduce

puts "--------------------------------"
puts "Listen:"
$p1 speak
$p2 speak
$p3 speak

puts "--------------------------------"
$p1 birthday
$p1 introduce

puts "================================"
