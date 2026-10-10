# 09_foreach_objects.tcl — Week 6 bonus: foreach over a list of objects
# Run: make week6-09
#      tclsh lessons/6/09_foreach_objects.tcl

oo::class create Pet {
    variable name kind

    constructor {n k} {
        set name $n
        set kind $k
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
set c [Pet new "Lucky" "dog"]

set shop [list $a $b $c]

puts "=== Pet shop speaks ==="
foreach p $shop {
    $p speak
}
