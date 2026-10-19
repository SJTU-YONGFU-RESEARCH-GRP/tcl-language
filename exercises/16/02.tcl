proc namesOfKind {records kind} {
    # 检查字段，不要猜名字
}
set cells [list     [dict create name U1 kind BUF area 0.5]     [dict create name U2 kind AND2 area 1.2]     [dict create name U3 kind BUF area 0.8]]
puts [namesOfKind $cells BUF]
