proc matchNames {names pattern} {
    set result {}
    foreach name $names {
        if {[string match $pattern $name]} { lappend result $name }
    }
    return $result
}
puts [matchNames {U_AND CLK_BUF U_BUF} U_*]
