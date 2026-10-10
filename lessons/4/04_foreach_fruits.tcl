# 04_foreach_fruits.tcl — Week 4 Day 2: foreach over a fruit list
# Run: make week4-04
#      tclsh lessons/4/04_foreach_fruits.tcl

set fruits [list apple banana cherry orange grape]

puts "=== Fruit list (foreach) ==="
foreach fruit $fruits {
    puts "I like $fruit."
}
