proc runReport {configPath} {
    # source 配置；检查字典及字段；source 工具；读数据；生成两个文件。
    error "请实现 runReport"
}
if {$argc != 1} {
    puts "error: usage: tclsh solution.tcl config.tcl"
} elseif {[catch {runReport [lindex $argv 0]} result]} {
    puts "error: $result"
} else {
    puts "valid=[dict get $result valid]"
}
