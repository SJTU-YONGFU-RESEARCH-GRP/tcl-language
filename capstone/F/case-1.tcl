# Execute after the project implementation: 改变配置阈值而不修改入口
set changed [runReport alternate.tcl]
puts "valid=[dict get $changed valid]; selected=[llength [dict get $changed selected]]; errors=[llength [dict get $changed errors]]"
puts [string trimright [reportTools::readText alternate-summary.txt] "\n"]
