proc pathSummary {records} {
    set negative 0
    set worst {}
    foreach record $records {
        set slack [dict get $record slack]
        if {$slack < 0} { incr negative }
        if {$worst eq "" || $slack < $worst} { set worst $slack }
    }
    return [dict create count [llength $records] negative $negative worst $worst]
}
set records [list [dict create path a slack 2.0] [dict create path b slack -0.5]]
set s [pathSummary $records]
puts "路径：[dict get $s count]；负值：[dict get $s negative]"
puts [format "最差：%.2f" [dict get $s worst]]
