set raw "  red ; ; BLUE; green  "
set rawEmpty " ;  ; "
set labels {}
foreach part [split $raw ";"] {
    set cleaned [string tolower [string trim $part]]
    if {$cleaned eq ""} {continue}
    lappend labels $cleaned
}
set emptyLabels {}
foreach part [split $rawEmpty ";"] {
    set cleaned [string tolower [string trim $part]]
    if {$cleaned eq ""} {continue}
    lappend emptyLabels $cleaned
}
set display [join $labels " / "]
puts $display
puts "空组：[llength $emptyLabels]"
