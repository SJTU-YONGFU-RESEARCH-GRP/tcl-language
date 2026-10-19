proc formatAverage {values digits} {
    set total 0.0
    foreach value $values { set total [expr {$total + $value}] }
    return [format "%.*f" $digits [expr {$total / [llength $values]}]]
}
