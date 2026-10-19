# Execute after the project implementation: 多种坏行与保留原始行号
set bad [runReport bad.tcl]
puts "valid=[dict get $bad valid]; selected=[llength [dict get $bad selected]]"
puts [string trimright [reportTools::readText bad-errors.txt] "\n"]
