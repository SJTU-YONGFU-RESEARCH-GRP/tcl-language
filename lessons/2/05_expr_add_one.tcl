# 05_expr_add_one.tcl — Week 2 Day 4: expr for age + 1
# Run: make week2-05
#      tclsh lessons/2/05_expr_add_one.tcl

set age 10
puts "This year I am $age years old."

# expr does math; curly braces inside expr are a good habit
set nextAge [expr {$age + 1}]
puts "Next year I will be $nextAge years old."
