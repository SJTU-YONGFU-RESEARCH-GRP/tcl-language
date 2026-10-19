proc selectCells {records pattern maxArea} {
    # 两个条件必须同时成立
}
set cells [list     [dict create name U_A kind AND2 area 1.2]     [dict create name U_B kind BUF area 0.5]     [dict create name CLK_B kind BUF area 0.4]]
set selected [selectCells $cells U_* 1.0]
puts "教学筛选：[llength $selected] 个"
foreach cell $selected { puts [dict get $cell name] }
