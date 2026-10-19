proc perPerson {total people} {
    if {![string is double -strict $total] || ![string is integer -strict $people]} {
        error "费用或人数不合法"
    }
    if {$total < 0 || $people <= 0} { error "费用或人数不合法" }
    return [expr {double($total) / $people}]
}
puts [format "人均：%.2f" [perPerson 10 4]]
if {[catch {perPerson 10 0} message]} { puts $message }
