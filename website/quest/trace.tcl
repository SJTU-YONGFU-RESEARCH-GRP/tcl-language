# Execution observers for teaching. They never evaluate user source fragments.
# @NS@ and @MARKER@ are fresh, private-to-this-run identifiers supplied by the Worker.
namespace eval @NS@ {
    variable busy 0
    variable enabled 0
    variable count 0
    variable watched {hero coins bag n total energy bottles each cells base power name hp numbers rows selected row hunger path slack violations worst value whole design period w h a b text raw chip}
}
proc @NS@::quote {value} {
    set value [string range $value 0 2047]
    set value [string map [list \\ \\\\ \" \\\" \n \\n \r \\r \t \\t] $value]
    regsub -all {[\x00-\x08\x0b\x0c\x0e-\x1f]} $value ? value
    return "\"$value\""
}
proc @NS@::listJSON {values} {
    set pieces {}
    foreach item [lrange $values 0 31] {lappend pieces [@NS@::quote $item]}
    return "\[[join $pieces ,]\]"
}
proc @NS@::rowsJSON {values} {
    set pieces {}
    foreach row [lrange $values 0 15] {
        if {[catch {@NS@::listJSON $row} encoded]} {set encoded {[]}}
        lappend pieces $encoded
    }
    return "\[[join $pieces ,]\]"
}
proc @NS@::deleted {old new op} {
    variable busy
    variable enabled
    variable count
    if {$busy || !$enabled || $count >= 256} {return}
    set busy 1
    catch {
        incr count
        set payload "{\"kind\":\"object-deleted\",\"phase\":\"leave\",\"code\":0,\"command\":[@NS@::quote [list $old destroy]],\"args\":[@NS@::listJSON [list $old destroy]],\"result\":\"\",\"index\":$count}"
        puts stderr "@MARKER@$payload"
    }
    variable busy 0
}
proc @NS@::enter {kind command op} { @NS@::observe $kind $command 0 {} enter }
proc @NS@::leave {kind command code value op} { @NS@::observe $kind $command $code $value leave }
proc @NS@::observe {kind command code value phase} {
    variable busy
    variable enabled
    variable count
    variable watched
    if {$busy || !$enabled || $count >= 256} {return}
    set busy 1
    # The observer must never change a command's completion code or value.
    catch {
        incr count
        set argv $command
        set candidates {}
        switch -- $kind {
            set - incr - lappend {set candidates [list [lindex $argv 1]]}
            foreach {set candidates [lindex $argv 1]}
            lassign {set candidates [lrange $argv 2 end]}
            regexp {set candidates [lrange $argv 3 end]}
        }
        foreach key $candidates {
            if {[regexp {^[A-Za-z_][A-Za-z0-9_:]*$} $key] && ![string match "@NS@::*" $key] && [lsearch -exact $watched $key] < 0 && [llength $watched] < 64} {lappend watched $key}
        }
        set vars {};set lists {};set records {}
        foreach key $watched {
            # Do not trigger a user-installed variable read trace by inspecting it.
            if {[llength [uplevel 2 [list trace info variable $key]]]} {continue}
            # Caller of the small enter/leave adapter is the user's actual scope.
            if {![uplevel 2 [list array exists $key]] && [uplevel 2 [list info exists $key]]} {
                set v [uplevel 2 [list set $key]]
                lappend vars "[@NS@::quote $key]:[@NS@::quote $v]"
                if {![catch {@NS@::listJSON $v} items]} {lappend lists "[@NS@::quote $key]:$items"}
                if {$key eq "rows" || $key eq "report"} {
                    if {![catch {@NS@::rowsJSON $v} items]} {lappend records "[@NS@::quote $key]:$items"}
                }
            }
        }
        set argLists {}
        foreach arg [lrange $argv 0 9] {
            if {[catch {@NS@::listJSON $arg} items]} {set items {[]}}
            lappend argLists $items
        }
        set resultList {[]}
        catch {set resultList [@NS@::listJSON $value]}
        set scope [uplevel 2 {namespace current}]
        set loopRows {[]}
        if {$kind eq "foreach" && [llength $argv] >= 3} {catch {set loopRows [@NS@::rowsJSON [lindex $argv 2]]}}
        set payload "{\"kind\":[@NS@::quote $kind],\"phase\":[@NS@::quote $phase],\"code\":$code,\"command\":[@NS@::quote $command],\"args\":[@NS@::listJSON $argv],\"argLists\":\[[join $argLists ,]\],\"loopRows\":$loopRows,\"resultList\":$resultList,\"scope\":[@NS@::quote $scope],\"result\":[@NS@::quote $value],\"vars\":{[join $vars ,]},\"lists\":{[join $lists ,]},\"records\":{[join $records ,]},\"index\":$count}"
        puts stderr "@MARKER@$payload"
        if {$phase eq "leave" && $code == 0} {
            # Newly defined procedures, classes, and objects also expose real returns.
            set target {}
            set type call
            if {$kind eq "proc"} {set target [uplevel 2 [list namespace which -command [lindex $argv 1]]]}
            if {$kind eq "oo::class" && [lindex $argv 1] eq "create"} {set target $value;set type class}
            if {$kind eq "class" && ([lindex $argv 1] eq "new" || [lindex $argv 1] eq "create")} {set target $value;set type object}
            if {$target ne "" && [llength [info commands $target]]} {
                catch {trace add execution $target leave [list @NS@::leave $type]}
                if {$type eq "object"} {catch {trace add command $target delete @NS@::deleted}}
            }
        }
    }
    variable busy 0
    return
}
foreach command {set incr puts expr list lappend lindex llength lassign foreach for while proc dict string open gets close catch error regexp source oo::class} {
    if {[llength [info commands ::$command]]} {
        trace add execution ::$command leave [list @NS@::leave $command]
    }
}
foreach command {foreach for while} {
    trace add execution ::$command enter [list @NS@::enter $command]
}
