# Execute after the project implementation: 缺配置字段和缺输入文件
catch {runReport incomplete.tcl} message; puts $message
puts "缺失输入报错: [catch {runReport missing.tcl}]"
