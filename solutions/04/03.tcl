set status "pending"
set people 0
set code "01"
if {$status eq "confirmed" && $people > 0} {
    set action "制作名牌"
} else {
    set action "核实报名"
}
set sameCode [expr {$code eq "1"}]
puts $action
puts $sameCode
