set count 6
set fee 100
# 用 incr 更新人数，再求平均
set average 0
puts "人数：$count"
puts [format "人均：%.2f" $average]
