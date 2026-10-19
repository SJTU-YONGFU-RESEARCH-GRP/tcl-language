proc expenseSummary {records} {
    # 返回 dict: count total totals rejected。
    # rejected 是 {序号 原因} 元素的列表。
    error "请实现逐条检查和类别累加"
}
proc printExpenses {records} {
    set result [expenseSummary $records]
    puts "合法记录: [dict get $result count]"
    dict for {category cents} [dict get $result totals] {puts "$category: $cents 分"}
}
set records [list [dict create category 餐食 cents 1850] [dict create category 交通 cents 320] [dict create category 餐食 cents 650] [dict create category 日用 cents -100] [dict create category 交通 cents abc]]
printExpenses $records
