proc generateReport {argsList} {
    if {[llength $argsList] != 1} { error "需要一个输入文件参数" }
    set config [source settings.tcl]
    source tools.tcl
    set ch [open [lindex $argsList 0] r]
    set values [split [string trim [read $ch]] "
"]
    close $ch
    set average [formatAverage $values [dict get $config digits]]
    return "[dict get $config title]
平均值：$average"
}
puts [generateReport $argv]
