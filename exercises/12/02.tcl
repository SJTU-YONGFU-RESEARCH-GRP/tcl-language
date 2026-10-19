proc perPerson {total people} {
    # 校验并返回浮点结果
}
puts [format "人均：%.2f" [perPerson 10 4]]
if {[catch {perPerson 10 0} message]} { puts $message }
