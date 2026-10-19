set times {12 8 15 0}
set total 0
set count 0
foreach minutes $times {
    set total [expr {$total + $minutes}]
    incr count
}
puts "$count 条，共 $total 分钟"
