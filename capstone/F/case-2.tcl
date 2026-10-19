# Execute after the project implementation: 空文件仍生成两个文件
set empty [runReport empty.tcl]
puts [string trimright [reportTools::readText empty-summary.txt] "\n"]
puts "Errors: [string trim [reportTools::readText empty-errors.txt]]"
