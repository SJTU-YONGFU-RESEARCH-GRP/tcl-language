# 08_braces_literal.tcl — Week 2 syntax lab: quotes, braces, [], backslash
# Run: make week2-08
#      tclsh lessons/2/08_braces_literal.tcl
#
# Five substitution rules (copy into your notebook):
#   "..."  — $ and [cmd] still run inside
#   {...}  — almost everything kept literal
#   $name  — read a variable
#   [cmd]  — run a command, paste its result
#   \x     — escape the next character

set name "Amy"
set age 10

puts "=== 1. double quotes vs braces ==="
puts "hello $name"
puts {hello $name}

puts "=== 2. command substitution \[expr\] ==="
puts "next year I will be [expr {$age + 1}]"

puts "=== 3. backslash escapes ==="
puts "dollar=\$name"
puts "line1\nline2"

puts "=== 4. when braces help ==="
puts {Print [brackets] and $dollars safely with braces.}
