proc writeSummary {inputPath outputPath} {
    set input [open $inputPath r]
    set count 0
    set total 0.0
    while {[gets $input line] >= 0} {
        set line [string trim $line]
        if {$line eq ""} { continue }
        incr count
        set total [expr {$total + $line}]
    }
    close $input
    set output [open $outputPath w]
    puts $output "数量：$count"
    if {$count == 0} {
        puts $output "平均值：无数据"
    } else {
        puts $output [format "平均值：%.2f" [expr {$total / $count}]]
    }
    close $output
    return $count
}
puts "已写入：[writeSummary measurements.txt report.txt] 条"
