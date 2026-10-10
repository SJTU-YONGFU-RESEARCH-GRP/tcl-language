# 06_class_and_object_words.tcl — Week 6: print class vs object story
# Run: make week6-06
#      tclsh lessons/6/06_class_and_object_words.tcl
#
# Pet = mold (class). Mimi and Buddy = toys (objects). speak = action (method).

oo::class create Pet {
    variable name

    constructor {n} {
        set name $n
    }

    method hello {} {
        puts "Hello from object $name"
    }
}

puts "=== Vocabulary demo ==="
puts "Class  : Pet (the mold)"
puts "Objects: two real pets made from the mold"
puts ""

set mimi [Pet new "Mimi"]
set buddy [Pet new "Buddy"]

$mimi hello
$buddy hello

puts ""
puts "Same class Pet, two different objects."
