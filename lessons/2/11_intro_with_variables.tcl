# 11_intro_with_variables.tcl — Week 2 bonus: self-intro using variables
# Run: make week2-11
#      tclsh lessons/2/11_intro_with_variables.tcl
# Change every set line to describe yourself.

set name "Amy"
set age 10
set school "Sunny Elementary"
set favoriteColor "blue"
set goal "Learn Tcl and later Calibre"

puts "================================"
puts "   SELF INTRO (with variables)"
puts "================================"
puts "Name   : $name"
puts "Age    : $age"
puts "School : $school"
puts "Color  : $favoriteColor"
puts "Goal   : $goal"
puts "================================"

set nextAge [expr {$age + 1}]
puts "Next year I will be $nextAge."
