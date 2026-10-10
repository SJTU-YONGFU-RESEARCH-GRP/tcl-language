# 04_proc_pass_fail.tcl — Week 5 Day 2: proc with if inside
# Run: make week5-04
#      tclsh lessons/5/04_proc_pass_fail.tcl

proc checkScore {subject score} {
    if {$score >= 60} {
        puts "$subject: Pass ($score)"
    } else {
        puts "$subject: Fail ($score)"
    }
}

checkScore "Math" 88
checkScore "English" 72
checkScore "Science" 55
