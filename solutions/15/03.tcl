oo::class create StatsMeter {
    variable readings
    constructor {} { set readings {} }
    method add {value} { lappend readings $value }
    method average {} {
        if {[llength $readings] == 0} { return {无数据} }
        set sum 0.0
        foreach value $readings { set sum [expr {$sum + $value}] }
        return [format "%.2f" [expr {$sum / [llength $readings]}]]
    }
    method reset {} { set readings {} }
}
set meter [StatsMeter new]
$meter add 2
$meter add 6
puts [$meter average]
$meter reset
puts [$meter average]
$meter destroy
