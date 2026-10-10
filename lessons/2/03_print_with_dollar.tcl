# 03_print_with_dollar.tcl — Week 2 Day 2: variables inside quoted strings
# Run: make week2-03
#      tclsh lessons/2/03_print_with_dollar.tcl

set name "Amy"
set city "Shanghai"

# Inside double quotes, $name is replaced with the box contents
puts "My name is $name."
puts "I live in $city."
puts "Hello, my name is $name and I live in $city."
