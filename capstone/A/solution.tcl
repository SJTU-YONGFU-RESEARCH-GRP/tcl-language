proc cleanRegistrations {names} {
    set clean {}
    foreach name $names {
        set name [string trim $name]
        regsub -all {[ \t\r\n]+} $name { } name
        if {$name ne ""} {lappend clean $name}
    }
    return [lsort -dictionary -unique $clean]
}
proc showRegistrations {names} {
    set clean [cleanRegistrations $names]
    puts "人数: [llength $clean]"
    foreach name $clean {puts $name}
}
set names [list "  Maya Chen  " "Lin Wei" "Maya\tChen" "  " "Chen Yu" "Lin  Wei"]
showRegistrations $names
