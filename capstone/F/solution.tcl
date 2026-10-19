proc runReport {configPath} {
    source -encoding utf-8 $configPath
    if {![info exists reportConfig]} {error "配置没有设置 reportConfig"}
    if {[catch {dict size $reportConfig}]} {error "reportConfig 必须是字典"}
    foreach key {tools input output errors minimum} {
        if {![dict exists $reportConfig $key]} {error "配置缺少字段: $key"}
    }
    source -encoding utf-8 [dict get $reportConfig tools]
    set minimum [reportTools::decimalNumber [dict get $reportConfig minimum]]
    set text [reportTools::readText [dict get $reportConfig input]]
    set result [reportTools::summarize $text $minimum]
    set selected [dict get $result selected]
    set summary [list "Teaching measurement summary" "Valid: [dict get $result valid]" "Selected: [llength $selected]" [format "Minimum: %.2f" $minimum]]
    foreach row $selected {
        lassign $row name value; lappend summary [format "%s: %.2f" $name $value]
    }
    set errors [dict get $result errors]
    if {![llength $errors]} {set errors [list "(none)"]}
    reportTools::writeText [dict get $reportConfig output] [join $summary "\n"]
    reportTools::writeText [dict get $reportConfig errors] [join $errors "\n"]
    dict set result output [dict get $reportConfig output]
    dict set result errorFile [dict get $reportConfig errors]
    return $result
}
if {$argc != 1} {
    puts "error: usage: tclsh solution.tcl config.tcl"
} elseif {[catch {runReport [lindex $argv 0]} result]} {
    puts "error: $result"
} else {
    puts "valid=[dict get $result valid]; selected=[llength [dict get $result selected]]; errors=[llength [dict get $result errors]]"
    puts "--- [dict get $result output] ---"
    puts [string trimright [reportTools::readText [dict get $result output]] "\n"]
    puts "--- [dict get $result errorFile] ---"
    puts [string trimright [reportTools::readText [dict get $result errorFile]] "\n"]
}
