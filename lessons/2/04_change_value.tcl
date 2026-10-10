# 04_change_value.tcl — Week 2 Day 3: change a variable and print again
# Run: make week2-04
#      tclsh lessons/2/04_change_value.tcl

set favoriteColor "blue"
puts "Before: my favorite color is $favoriteColor"

# Put a new value into the same box (same label)
set favoriteColor "green"
puts "After : my favorite color is $favoriteColor"

set age 10
puts "I am $age years old."
set age 11
puts "Next year I will be $age years old."
