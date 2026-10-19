proc parseTeachingPath {line period} {
    if {![regexp {^PATH\s+(\S+)\s+DELAY\s+([0-9]+(?:\.[0-9]+)?)$} $line -> path delay]} {
        error "教学路径格式错误"
    }
    return [dict create path $path delay $delay slack [expr {double($period) - $delay}]]
}
set record [parseTeachingPath {PATH p7 DELAY 10.2} 10]
puts "[dict get $record path]：[format %.2f [dict get $record slack]]"
