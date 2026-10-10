# 08_braces_literal.tcl — Week 2: curly braces stop $ substitution
# Run: make week2-08
#      tclsh lessons/2/08_braces_literal.tcl

set name "Amy"

# Double quotes: $name is replaced
puts "Hello, $name!"

# Curly braces: print exactly what is inside (no $ substitution)
puts {Hello, $name!}

# Useful when you want a literal dollar sign in output
set price 5
puts "Price is $$price dollars today."
puts {The variable is called $name in this lesson.}
