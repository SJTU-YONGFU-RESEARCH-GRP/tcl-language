set samples [list {temp=-8} {temp=0} {temp=bad}]
set values {}
set rejected {}
# 每行成功才读取捕获值
puts "有效：[join $values {, }]"
puts "拒绝：[join $rejected {, }]"
