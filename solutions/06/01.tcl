set names [list "顾 宁" "Ari Lee" 吴涛]
lappend names "周 月"
set second [lindex $names 1]
set count [llength $names]
puts "$count 人，第二位：$second"
