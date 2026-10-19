proc measurementNumber {value} {
    if {![regexp {^[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$} $value]} {
        error "不是有限十进制数: $value"
    }
    set number [scan $value %f]
    if {![expr {abs($number) < Inf}]} {error "不是有限十进制数: $value"}
    return $number
}
proc measurementStats {values lower upper} {
    set lower [measurementNumber $lower]; set upper [measurementNumber $upper]
    if {$lower > $upper} {error "下界不能大于上界"}
    set count 0; set minimum ""; set maximum ""; set sum 0.0; set outside {}
    foreach raw $values {
        incr count
        if {[catch {measurementNumber $raw} value]} {error "元素 $count: $value"}
        if {$count == 1 || $value < $minimum} {set minimum $value}
        if {$count == 1 || $value > $maximum} {set maximum $value}
        set sum [expr {$sum + $value}]
        if {![expr {abs($sum) < Inf}]} {error "累计值超出浮点范围"}
        if {$value < $lower || $value > $upper} {lappend outside $raw}
    }
    set mean ""
    if {$count > 0} {set mean [expr {$sum / $count}]}
    return [dict create count $count minimum $minimum maximum $maximum mean $mean outside $outside]
}
proc showMeasurements {values lower upper} {
    set result [measurementStats $values $lower $upper]
    puts "数量: [dict get $result count]"
    foreach {key label} {minimum 最小值 maximum 最大值 mean 平均值} {
        set value [dict get $result $key]
        if {$value eq ""} {puts "$label: N/A"} else {puts [format "%s: %.2f" $label $value]}
    }
    set outside [dict get $result outside]
    puts "越界数: [llength $outside]"
    if {[llength $outside]} {puts "越界值: [join $outside {, }]"}
}
showMeasurements {9.5 10 10.5 13} 9 12
