source report-tools.tcl
proc buildAnalysis {paths period outputPath} {
    # 生成状态、路径数、负 slack 数、最差 slack
}
set result [buildAnalysis {morning.rpt evening.rpt} 10 analysis.txt]
set ch [open analysis.txt r]
puts [string trim [read $ch]]
close $ch
