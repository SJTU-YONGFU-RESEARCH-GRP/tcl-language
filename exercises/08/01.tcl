set sample [dict create id S-08 status waiting count 4]
# 更新两个字段，不覆盖整条记录
puts "[dict get $sample status] / [dict get $sample count]"
