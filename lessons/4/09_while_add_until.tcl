# 09_while_add_until.tcl — Week 4 Day 4: while keeps going until a goal
# Run: make week4-09
#      tclsh lessons/4/09_while_add_until.tcl

set total 0
set step 1

puts "=== Add 1 each time until total >= 10 ==="

while {$total < 10} {
    puts "total is $total — adding $step"
    set total [expr {$total + $step}]
}

puts "Stopped at total = $total"
