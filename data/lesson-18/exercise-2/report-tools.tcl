proc parseReport {path period} {
    if {![regexp {^[0-9]+(?:\.[0-9]+)?$} $period]} {
        error "周期必须是正十进制数"
    }
    scan $period %f period
    if {$period <= 0 || $period > 1000} { error "周期须满足 0 < period <= 1000 ns" }
    set ch [open $path r]
    set status [catch {
        set records {}
        set lineNo 0
        while {[gets $ch line] >= 0} {
            incr lineNo
            set line [string trim $line]
            if {$line eq "" || [string match #* $line]} { continue }
            if {![regexp {^PATH\s+(\S+)\s+DELAY\s+([0-9]+(?:\.[0-9]+)?)$} $line -> name delay]} {
                error "$path:$lineNo：教学路径格式错误"
            }
            scan $delay %f delay
            if {$delay > 1000} { error "$path:$lineNo：延迟超出教学范围" }
            lappend records [dict create source $path line $lineNo path $name delay $delay slack [expr {$period - $delay}]]
        }
        set records
    } result options]
    close $ch
    if {$status != 0} { return -options $options $result }
    return $result
}
proc collectReports {paths period} {
    set records {}
    set issues {}
    set loaded 0
    foreach path $paths {
        if {[catch {parseReport $path $period} one]} {
            lappend issues [dict create source $path message $one]
        } else {
            incr loaded
            foreach record $one { lappend records $record }
        }
    }
    return [dict create records $records issues $issues loaded $loaded]
}
proc summarizeRecords {records} {
    set count [llength $records]
    set negative 0
    set worst {}
    foreach record $records {
        set slack [dict get $record slack]
        if {$slack < 0} { incr negative }
        if {$worst eq "" || $slack < $worst} { set worst $slack }
    }
    return [dict create count $count negative $negative worst $worst]
}
