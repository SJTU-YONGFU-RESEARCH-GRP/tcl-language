source report-tools.tcl
proc writeIssues {paths period outputPath} {
    set result [collectReports $paths $period]
    set output [open $outputPath w]
    foreach issue [dict get $result issues] {
        puts $output "[dict get $issue source] | [dict get $issue message]"
    }
    close $output
    return $result
}
set result [writeIssues {morning.rpt bad.rpt empty.rpt} 10 errors.txt]
puts "成功：[dict get $result loaded]；失败：[llength [dict get $result issues]]"
