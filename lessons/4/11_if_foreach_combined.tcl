# 11_if_foreach_combined.tcl — Week 4 bonus: foreach + if together
# Run: make week4-11
#      tclsh lessons/4/11_if_foreach_combined.tcl

set scores [list 92 55 78 88 61]

puts "=== Pass / Fail for each score ==="

foreach score $scores {
    if {$score >= 60} {
        puts "$score : Pass"
    } else {
        puts "$score : Fail"
    }
}

set passCount 0
foreach score $scores {
    if {$score >= 60} {
        incr passCount
    }
}

puts "Passed: $passCount out of [llength $scores]"
