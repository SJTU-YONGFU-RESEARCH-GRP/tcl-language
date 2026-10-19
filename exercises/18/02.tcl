source report-tools.tcl
proc writeIssues {paths period outputPath} {
    # 收集文件并写入错误清单，最后返回字典
}
set result [writeIssues {morning.rpt bad.rpt empty.rpt} 10 errors.txt]
puts "成功：[dict get $result loaded]；失败：[llength [dict get $result issues]]"
