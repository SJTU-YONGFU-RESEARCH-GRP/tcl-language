# 08_while_countdown.tcl — Week 4 Day 4: while loop counts down 5 to 1
# Run: make week4-08
#      tclsh lessons/4/08_while_countdown.tcl

set n 5

puts "=== Countdown ==="
while {$n > 0} {
    puts $n
    incr n -1
}

puts "Launch!"
