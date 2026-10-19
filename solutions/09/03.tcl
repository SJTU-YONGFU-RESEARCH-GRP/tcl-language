set lines [list {08:00 value=12 status=OK} {08:01 value=-2 status=WARN} {08:02 value=0 status=ERROR} ""]
set pattern {^([0-9]{2}:[0-9]{2}) value=(-?[0-9]+) status=(OK|WARN|ERROR)$}
set records {}
set attention {}
set rejectedCount 0
foreach line $lines {
    if {![regexp -- $pattern $line whole time value status]} {
        incr rejectedCount
        continue
    }
    lappend records [dict create time $time value $value status $status]
    if {$status eq "WARN" || $status eq "ERROR"} {
        lappend attention $time
    }
}
puts "记录：[llength $records]"
puts "关注：[join $attention {, }]"
puts "拒绝：$rejectedCount"
