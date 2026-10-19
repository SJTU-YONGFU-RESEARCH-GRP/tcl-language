proc expenseSummary {records} {
    set totals {}; set rejected {}; set count 0; set total 0; set index 0
    foreach row $records {
        incr index
        set reason ""
        if {[catch {dict size $row}]} {
            set reason "不是合法字典"
        } elseif {![dict exists $row category] || ![dict exists $row cents]} {
            set reason "缺少 category 或 cents"
        } else {
            set category [string trim [dict get $row category]]
            set cents [dict get $row cents]
            if {$category eq ""} {
                set reason "类别为空"
            } elseif {![string is entier -strict $cents] || $cents < 0} {
                set reason "金额必须是非负整数分"
            }
        }
        if {$reason ne ""} {lappend rejected [list $index $reason]; continue}
        dict incr totals $category $cents
        incr total $cents
        incr count
    }
    return [dict create count $count total $total totals $totals rejected $rejected]
}
proc printExpenses {records} {
    set result [expenseSummary $records]
    puts "合法记录: [dict get $result count]"
    set totals [dict get $result totals]
    foreach category [lsort -dictionary [dict keys $totals]] {
        puts [format "%s: %.2f 元" $category [expr {[dict get $totals $category] / 100.0}]]
    }
    puts [format "总额: %.2f 元" [expr {[dict get $result total] / 100.0}]]
    puts "拒绝记录: [llength [dict get $result rejected]]"
    foreach item [dict get $result rejected] {
        lassign $item index reason
        puts "记录 $index: $reason"
    }
}
set records [list [dict create category 餐食 cents 1850] [dict create category 交通 cents 320] [dict create category 餐食 cents 650] [dict create category 日用 cents -100] [dict create category 交通 cents abc]]
printExpenses $records
