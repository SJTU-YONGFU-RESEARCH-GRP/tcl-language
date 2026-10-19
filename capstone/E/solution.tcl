proc pathNumber {value} {
    if {![regexp {^[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$} $value]} {error "数值必须是有限十进制数"}
    set number [scan $value %f]
    if {![expr {abs($number) < Inf}]} {error "数值必须是有限十进制数"}
    return $number
}
proc parsePaths {text} {
    set paths {}; set rejected {}; set line 0
    foreach raw [split $text "\n"] {
        incr line; set raw [string trim $raw]
        if {$raw eq "" || [string match {#*} $raw]} {continue}
        set reason ""
        if {![regexp {^path=([A-Za-z0-9_.:/-]+) +delay=(\S+) +slack=(\S+)$} $raw full name delay slack]} {
            set reason "格式不符"
        } elseif {[catch {pathNumber $delay} delayValue] || [catch {pathNumber $slack} slackValue]} {
            set reason "数值必须是有限十进制数"
        } elseif {$delayValue < 0} {
            set reason "delay 不能为负"
        }
        if {$reason ne ""} {lappend rejected [list $line $reason]; continue}
        lappend paths [dict create name $name delay $delayValue slack $slackValue]
    }
    return [dict create paths $paths rejected $rejected]
}
proc selectPaths {paths {threshold 0}} {
    set threshold [pathNumber $threshold]
    set decorated {}
    foreach path $paths {
        set slack [dict get $path slack]
        if {$slack < $threshold} {lappend decorated [list $slack [dict get $path name] $path]}
    }
    # lsort 稳定排序：先确定同 slack 时的姓名顺序，再按 slack 排。
    set decorated [lsort -dictionary -index 1 $decorated]
    set decorated [lsort -real -index 0 $decorated]
    set selected {}
    foreach item $decorated {lappend selected [lindex $item 2]}
    return $selected
}
proc showPathReport {text} {
    set result [parsePaths $text]
    set selected [selectPaths [dict get $result paths]]
    puts "教学路径报告 / ns / 非真实 STA"
    puts "合法路径: [llength [dict get $result paths]]"
    puts "负 slack 路径: [llength $selected]"
    puts "path | delay | slack"
    foreach path $selected {
        puts [format "%s | %.2f | %.2f" [dict get $path name] [dict get $path delay] [dict get $path slack]]
    }
    if {![llength $selected]} {puts "(无负 slack 路径)"}
    puts "非法行: [llength [dict get $result rejected]]"
    foreach rejected [dict get $result rejected] {
        lassign $rejected line reason; puts "行 $line: $reason"
    }
}
set channel [open paths.txt r]
set text [read $channel]; close $channel
showPathReport $text
