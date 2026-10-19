proc selectCells {records pattern maxArea} {
    set result {}
    foreach cell $records {
        if {[string match $pattern [dict get $cell name]] && [dict get $cell area] <= $maxArea} {
            lappend result $cell
        }
    }
    return $result
}
set cells [list     [dict create name U_A kind AND2 area 1.2]     [dict create name U_B kind BUF area 0.5]     [dict create name CLK_B kind BUF area 0.4]]
set selected [selectCells $cells U_* 1.0]
puts "教学筛选：[llength $selected] 个"
foreach cell $selected { puts [dict get $cell name] }
