set contacts [list " A@EXAMPLE.ORG " "B@other.org" "   " "c@example.org"]
 set selected {}
 # 清理后筛选
 puts [join $selected "\n"]
 puts "数量：[llength $selected]"
