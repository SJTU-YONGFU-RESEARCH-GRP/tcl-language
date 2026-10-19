proc cleanRegistrations {names} {
    # 1. 建立空列表；2. foreach 清理；3. 去重并排序。
    error "请实现 cleanRegistrations"
}
proc showRegistrations {names} {
    set clean [cleanRegistrations $names]
    puts "人数: [llength $clean]"
    foreach name $clean {puts $name}
}
set names [list "  Maya Chen  " "Lin Wei" "Maya\tChen" "  " "Chen Yu" "Lin  Wei"]
showRegistrations $names
