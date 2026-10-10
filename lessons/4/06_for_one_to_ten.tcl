# 06_for_one_to_ten.tcl — Week 4 Day 3: for loop prints 1 to 10
# Run: make week4-06
#      tclsh lessons/4/06_for_one_to_ten.tcl

puts "=== Count 1 to 10 ==="

for {set i 1} {$i <= 10} {incr i} {
    puts $i
}

puts "Done counting."
