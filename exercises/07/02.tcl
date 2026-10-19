set raw "  red ; ; BLUE; green  "
set rawEmpty " ;  ; "
set labels {}
set emptyLabels {}
# 切分后逐段清理，空段不要追加
set display [join $labels " / "]
puts $display
puts "空组：[llength $emptyLabels]"
