proc namesOfKind {records kind} {
    set result {}
    foreach cell $records {
        if {[dict get $cell kind] eq $kind} {
            lappend result [dict get $cell name]
        }
    }
    return $result
}
set cells [list     [dict create name U1 kind BUF area 0.5]     [dict create name U2 kind AND2 area 1.2]     [dict create name U3 kind BUF area 0.8]]
puts [namesOfKind $cells BUF]
