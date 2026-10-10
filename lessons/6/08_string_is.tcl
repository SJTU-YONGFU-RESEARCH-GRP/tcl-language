# 08_string_is.tcl — Week 6: string is <class>
# Run: make week6-08

foreach {val cls} {
  42 integer
  3.14 double
  true boolean
  hello alpha
  hello123 alnum
  {} space
} {
  puts [format "string is %-8s %-10s -> %s" $cls $val [string is $cls -strict $val]]
}
puts "Tip: without -strict, empty string is often 'true' for many classes."
exit
