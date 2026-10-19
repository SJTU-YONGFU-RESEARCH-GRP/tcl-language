set lines [list {08:00 value=12 status=OK} {08:01 value=-2 status=WARN} {08:02 value=0 status=ERROR} ""]
set pattern {^([0-9]{2}:[0-9]{2}) value=(-?[0-9]+) status=(OK|WARN|ERROR)$}
set records {}
set attention {}
set rejectedCount 0
# 解析、构造记录并按状态筛选
puts "记录：[llength $records]"
puts "关注：[join $attention {, }]"
puts "拒绝：$rejectedCount"
