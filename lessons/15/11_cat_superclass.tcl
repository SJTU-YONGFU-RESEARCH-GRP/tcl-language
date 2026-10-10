# 11_cat_superclass.tcl — Week 15 bonus: subclass with superclass
# Run: make week15-11
#      tclsh lessons/15/11_cat_superclass.tcl

oo::class create Pet {
    variable name

    constructor {n} {
        set name $n
    }

    method introduce {} {
        puts "I am $name."
    }
}

oo::class create Cat {
    superclass Pet

    method speak {} {
        variable name
        puts "$name: meow!"
    }
}

set mimi [Cat new "Mimi"]
$mimi introduce
$mimi speak

puts "Cat is a more specialized mold built from Pet."
