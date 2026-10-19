proc readCounts {path} {
    # 打开文件，校验，关闭通道；失败应继续报错
}
puts "接收：[readCounts good.txt]"
if {[catch {readCounts bad.txt} message]} { puts $message }
