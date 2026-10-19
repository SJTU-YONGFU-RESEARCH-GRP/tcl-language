proc formatAverage {values digits} {
    if {[llength $values] == 0} { return {无数据} }
    set total 0.0
    foreach value $values { set total [expr {$total + $value}] }
    return [format "%.*f" $digits [expr {$total / [llength $values]}]]
}
