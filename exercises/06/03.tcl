set names [list "周 月" "顾 宁" "周 月" "Ari Lee" "顾 宁"]
set unique {}
set emptyNames {}
set emptyUnique {}
# 对每个姓名，仅在未出现时追加
puts "[llength $unique] 人：[join $unique { / }]"
puts "空名单：[llength $emptyUnique] 人"
