# 07_constructor_args.tcl — Week 15: constructor stores multiple fields
# Run: make week15-07
#      tclsh lessons/15/07_constructor_args.tcl

oo::class create Student {
    variable name grade school

    constructor {n g s} {
        set name $n
        set grade $g
        set school $s
    }

    method card {} {
        puts "Name   : $name"
        puts "Grade  : $grade"
        puts "School : $school"
    }
}

set s [Student new "Amy" "5" "Sunny Elementary"]
$s card
