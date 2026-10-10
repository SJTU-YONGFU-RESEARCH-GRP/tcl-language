# 11_proc_double.tcl — Week 5 bonus: proc calling return value
# Run: make week5-11
#      tclsh lessons/5/11_proc_double.tcl

proc double {n} {
    return [expr {$n * 2}]
}

proc showDouble {label n} {
    set result [double $n]
    puts "$label: $n doubled is $result"
}

showDouble "A" 5
showDouble "B" 12
showDouble "C" [double 3]
