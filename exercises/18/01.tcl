proc pathSummary {records} {
    # 统计数量、负值数量与最小值
}
set records [list [dict create path a slack 2.0] [dict create path b slack -0.5]]
set s [pathSummary $records]
puts "路径：[dict get $s count]；负值：[dict get $s negative]"
puts [format "最差：%.2f" [dict get $s worst]]
