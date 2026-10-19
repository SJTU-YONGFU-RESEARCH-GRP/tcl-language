set readings {9 14 35 41 12}
set limit 30
set visited 0
set found "未发现"
foreach value $readings {
    incr visited
    if {$value > $limit} {
        set found $value
        break
    }
}
puts "检查 $visited 条，首个越界：$found"
