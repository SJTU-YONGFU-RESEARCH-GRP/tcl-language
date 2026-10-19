proc requireCount {text} {
    # 检查格式和范围
}
puts [requireCount 0]
if {[catch {requireCount -2} message]} { puts $message }
