# 11_puts_without_newline.tcl — bonus: puts -nonewline
# Run: tclsh lessons/1/11_puts_without_newline.tcl
# Normal puts adds a newline. -nonewline keeps printing on the same line.

puts -nonewline "Loading"
puts -nonewline "."
puts -nonewline "."
puts -nonewline "."
puts ""
puts "Done! (that empty puts above finished the line)"
