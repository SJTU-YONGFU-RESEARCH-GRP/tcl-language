proc readCounts {path} {
    set ch [open $path r]
    set status [catch {
        set values {}
        set lineNo 0
        while {[gets $ch line] >= 0} {
            incr lineNo
            set line [string trim $line]
            if {$line eq ""} { continue }
            if {![string is integer -strict $line] || $line < 0} {
                error "第 $lineNo 行不是非负整数"
            }
            lappend values $line
        }
        set values
    } result options]
    close $ch
    if {$status != 0} { return -options $options $result }
    return $result
}
puts "接收：[readCounts good.txt]"
if {[catch {readCounts bad.txt} message]} { puts $message }
