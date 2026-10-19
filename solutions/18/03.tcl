source report-tools.tcl
proc buildAnalysis {paths period outputPath} {
    set result [collectReports $paths $period]
    set summary [summarizeRecords [dict get $result records]]
    set status "完整"
    if {[llength [dict get $result issues]] > 0} { set status "部分" }
    set worst [dict get $summary worst]
    if {$worst eq ""} {
        set displayed "无数据"
    } else {
        set displayed [format "%.2f ns" $worst]
    }
    set out [open $outputPath w]
    puts $out "教学摘要：$status"
    puts $out "路径：[dict get $summary count]"
    puts $out "负 slack：[dict get $summary negative]"
    puts $out "最差 slack：$displayed"
    close $out
    return $result
}
set result [buildAnalysis {morning.rpt evening.rpt} 10 analysis.txt]
set ch [open analysis.txt r]
puts [string trim [read $ch]]
close $ch
