# Execute after the project implementation: 可修改阈值但不改变数据
set parsed [parsePaths "path=N delay=4 slack=-0.1\npath=P delay=3 slack=0.4"]
puts "阈值 0.5: [llength [selectPaths [dict get $parsed paths] 0.5]]"
