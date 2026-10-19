proc countLines {path} {
    set ch [open $path r]
    set count 0
    while {[gets $ch line] >= 0} {
        if {[string trim $line] ne ""} { incr count }
    }
    close $ch
    return $count
}
puts [countLines readings.txt]
