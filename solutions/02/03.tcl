set count 6
set fee 100
incr count 3
incr count -1
set average [expr {double($fee) / $count}]
puts "人数：$count"
puts [format "人均：%.2f" $average]
