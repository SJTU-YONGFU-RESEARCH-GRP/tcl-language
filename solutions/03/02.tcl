set price 9
set quantity 4
set message "总计 [expr {$price * $quantity}] 元"
set formula {[expr {9 * 4}]}
puts $message
puts $formula
