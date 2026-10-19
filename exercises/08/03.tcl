array set temperatures {roomA 22 roomB 25}
# 更新数组并打印
set snapshot [dict create]
# 将数组转为字典快照并更新快照
puts "快照 roomB：[dict exists $snapshot roomB]"
