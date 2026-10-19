proc parseTeachingPath {line period} {
    # regexp 提取字段并返回字典
}
set record [parseTeachingPath {PATH p7 DELAY 10.2} 10]
puts "[dict get $record path]：[format %.2f [dict get $record slack]]"
