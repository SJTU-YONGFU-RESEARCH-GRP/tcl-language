set names [list "周 月" "顾 宁" "周 月" "Ari Lee" "顾 宁"]
set unique {}
foreach name $names {
    if {[lsearch -exact $unique $name] == -1} {
        lappend unique $name
    }
}
set emptyNames {}
set emptyUnique {}
foreach name $emptyNames {
    if {[lsearch -exact $emptyUnique $name] == -1} {
        lappend emptyUnique $name
    }
}
puts "[llength $unique] 人：[join $unique { / }]"
puts "空名单：[llength $emptyUnique] 人"
