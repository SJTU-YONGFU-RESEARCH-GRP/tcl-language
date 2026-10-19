namespace eval bus {
    proc fee {n} { return [expr {$n * 8}] }
}
namespace eval snack {
    proc fee {n} { return [expr {$n * 5}] }
}
puts [::bus::fee 4]
puts [::snack::fee 4]
