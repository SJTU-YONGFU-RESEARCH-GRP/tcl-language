namespace eval reportTools {
    proc decimalNumber {value} {
        if {![regexp {^[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$} $value]} {error "数值不是有限十进制数"}
        set number [scan $value %f]
        if {![expr {abs($number) < Inf}]} {error "数值不是有限十进制数"}
        return $number
    }
    proc readText {path} {
        set channel [open $path r]
        fconfigure $channel -encoding utf-8
        try {return [read $channel]} finally {close $channel}
    }
    proc writeText {path text} {
        set channel [open $path w]
        fconfigure $channel -encoding utf-8
        try {puts $channel $text} finally {close $channel}
    }
    proc summarize {text minimum} {
        set minimum [decimalNumber $minimum]
        set valid 0; set selected {}; set errors {}; set line 0
        foreach raw [split $text "\n"] {
            incr line; set raw [string trim $raw]
            if {$raw eq "" || [string match {#*} $raw]} {continue}
            set fields [split $raw ,]
            if {[llength $fields] != 2} {lappend errors "line $line: expected name,value"; continue}
            lassign $fields name value
            set name [string trim $name]; set value [string trim $value]
            if {$name eq ""} {lappend errors "line $line: empty name"; continue}
            if {[catch {decimalNumber $value} number]} {lappend errors "line $line: invalid number"; continue}
            incr valid
            if {$number >= $minimum} {lappend selected [list $name $number]}
        }
        return [dict create valid $valid selected $selected errors $errors minimum $minimum]
    }
}
