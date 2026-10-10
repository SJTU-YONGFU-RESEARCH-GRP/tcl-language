# 03_proc_add_return.tcl — Week 5 Day 2: proc with return
# Run: make week5-03
#      tclsh lessons/5/03_proc_add_return.tcl

proc add {a b} {
    return [expr {$a + $b}]
}

set sum [add 15 4]
puts "15 + 4 = $sum"

set total [add 88 92]
puts "88 + 92 = $total"
