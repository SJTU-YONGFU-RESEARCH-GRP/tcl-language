proc diagnoseLog {text {radius 1}} {
    if {![string is integer -strict $radius] || $radius < 0 || $radius > 20} {error "上下文行数必须是 0..20 的整数"}
    set counts [dict create INFO 0 WARN 0 ERROR 0]
    set incidents {}; set invalid {}
    set text [string trimright $text "\n"]
    if {$text eq ""} {return [dict create counts $counts incidents $incidents invalid $invalid]}
    set lines [split $text "\n"]
    for {set i 0} {$i < [llength $lines]} {incr i} {
        set raw [string trimright [lindex $lines $i] "\r"]
        if {![regexp {^([0-9]{2}):([0-9]{2}):([0-9]{2}) (INFO|WARN|ERROR) (.+)$} $raw whole h m s level message] ||
            [scan $h %d] > 23 || [scan $m %d] > 59 || [scan $s %d] > 59} {
            lappend invalid [expr {$i + 1}]; continue
        }
        dict incr counts $level
        if {$level eq "INFO"} {continue}
        set context {}
        set begin [expr {max(0, $i - $radius)}]
        set end [expr {min([llength $lines] - 1, $i + $radius)}]
        for {set j $begin} {$j <= $end} {incr j} {
            lappend context [list [expr {$j + 1}] [string trimright [lindex $lines $j] "\r"]]
        }
        lappend incidents [dict create line [expr {$i + 1}] level $level message $message context $context]
    }
    return [dict create counts $counts incidents $incidents invalid $invalid]
}
proc showDiagnosis {text {radius 1}} {
    set result [diagnoseLog $text $radius]
    puts "日志诊断 (教学样本)"
    puts "ERROR: [dict get $result counts ERROR]; WARN: [dict get $result counts WARN]"
    puts "格式错误行: [llength [dict get $result invalid]]"
    if {[llength [dict get $result invalid]]} {puts "行号: [join [dict get $result invalid] {, }]"}
    foreach item [dict get $result incidents] {
        puts "[dict get $item level] L[dict get $item line]: [dict get $item message]"
        foreach row [dict get $item context] {
            lassign $row line raw
            set marker " "
            if {$line == [dict get $item line]} {set marker "*"}
            puts [format "%s %d | %s" $marker $line $raw]
        }
    }
}
set log "09:00:00 INFO start\n09:00:01 INFO read input\n09:00:02 WARN slow read\n09:00:03 INFO retry\n09:00:04 ERROR missing result\n09:00:05 INFO stop"
showDiagnosis $log
