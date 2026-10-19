namespace eval ::__ws {variable busy 0;variable count 0}
proc ::__ws::quote {s} {
 set s [string map [list \\ \\\\ \" \\\" \n \\n \r \\r \t \\t] $s]
 regsub -all {[\x00-\x08\x0b\x0c\x0e-\x1f]} $s ? s
 return "\"$s\""
}
proc ::__ws::listjson {value} {set a {};foreach v [lrange $value 0 63] {lappend a [::__ws::quote [string range $v 0 1023]]};return "\[[join $a ,]\]"}
proc ::__ws::observe {command code result op} {
 variable busy;variable count
 if {$busy || $count>=120} {return}
 set busy 1
 catch {incr count;puts stderr "__WS_EVENT__{\"command\":[::__ws::quote [string range $command 0 1023]],\"result\":[::__ws::quote [string range $result 0 1023]],\"code\":$code}"}
 set busy 0
 return
}
proc ::__ws::objectNames {} {
 # Walk real class relationships, including unnamed instances under ::oo.
 # Classes and instances which existed before learner code are recorded below.
 if {![llength [info commands ::oo::object]]} {return {}}
 set pending [list ::oo::object];set seen {};set objects {};set visits 0
 while {[llength $pending] && $visits < 256} {
  set class [lindex $pending 0];set pending [lrange $pending 1 end]
  if {[dict exists $seen $class]} {continue}
  dict set seen $class 1;incr visits
  if {![catch {info class instances $class} instances]} {lappend objects {*}$instances}
  if {![catch {info class subclasses $class} children]} {lappend pending {*}$children}
 }
 return [lsort -unique $objects]
}
namespace eval ::__ws {variable baselineObjects [::__ws::objectNames]}
proc ::__ws::userNamespaces {} {
 set pending [list ::];set result {};set visits 0
 while {[llength $pending] && $visits < 128} {
  set space [lindex $pending 0];set pending [lrange $pending 1 end];incr visits
  if {$space in {::__ws ::tcl ::oo} || [string match {::__ws::*} $space] || [string match {::tcl::*} $space] || [string match {::oo::*} $space]} {continue}
  if {$space ne "::"} {lappend result $space}
  lappend pending {*}[lsort [namespace children $space]]
 }
 return $result
}
proc ::__ws::variableJson {fullName displayName} {
 # Query traces before reading; array-element read traces also remain untouched.
 if {[catch {uplevel #0 [list trace info variable $fullName]} traces] || [llength $traces]} {return ""}
 if {[uplevel #0 [list array exists $fullName]]} {
  set value {};set kind array
  foreach key [lrange [lsort [uplevel #0 [list array names $fullName]]] 0 63] {
   set element ${fullName}($key)
   if {[llength [uplevel #0 [list trace info variable $element]]]} {continue}
   if {[catch {uplevel #0 [list set $element]} item]} {continue}
   lappend value $key [string range $item 0 1023]
  }
 } else {
  if {[catch {uplevel #0 [list set $fullName]} value]} {return ""}
  set kind value
 }
 set items {[]};catch {set items [::__ws::listjson $value]}
 return "{\"name\":[::__ws::quote $displayName],\"value\":[::__ws::quote [string range $value 0 4095]],\"kind\":[::__ws::quote $kind],\"items\":$items}"
}
proc ::__ws::snapshot {} {
 variable baselineObjects
 set a {};set seen {}
 foreach v [lsort [info globals]] {
  if {[string match __* $v] || [string match tcl* $v] || $v in {env argv argc argv0 auto_path auto_index errorCode errorInfo workshop_stdout}} {continue}
  set fullName ::$v;set entry [::__ws::variableJson $fullName $v]
  if {$entry ne ""} {lappend a $entry;dict set seen $fullName 1}
  if {[llength $a] >= 64} {return "\[[join $a ,]\]"}
 }
 foreach space [::__ws::userNamespaces] {
  # Tcl resolves the namespace portion literally; only the variable tail is a glob.
  foreach fullName [lsort [info vars ${space}::*]] {
   if {[dict exists $seen $fullName]} {continue}
   set entry [::__ws::variableJson $fullName $fullName]
   if {$entry ne ""} {lappend a $entry;dict set seen $fullName 1}
   if {[llength $a] >= 64} {return "\[[join $a ,]\]"}
  }
 }
 foreach object [::__ws::objectNames] {
  if {$object in $baselineObjects} {continue}
  if {[catch {info object namespace $object} space] || [catch {info object vars $object} names]} {continue}
  foreach name [lsort $names] {
   set fullName ${space}::$name
   if {[dict exists $seen $fullName]} {continue}
   set entry [::__ws::variableJson $fullName $fullName]
   if {$entry ne ""} {lappend a $entry;dict set seen $fullName 1}
   if {[llength $a] >= 64} {return "\[[join $a ,]\]"}
  }
 }
 return "\[[join $a ,]\]"
}
proc ::__ws::files {{base .}} {
 set a {}
 foreach f [lsort [glob -nocomplain -directory $base *]] {
  if {[file isdirectory $f]} {set nested [::__ws::files $f];if {$nested ne "[]"} {lappend a [string range $nested 1 end-1]};continue}
  if {[file size $f]>65536} {set content {File exceeds 64 KiB preview limit}} else {set ch [open $f r];set content [read $ch];close $ch}
  lappend a "{\"name\":[::__ws::quote $f],\"content\":[::__ws::quote $content]}"
 }
 return "\[[join $a ,]\]"
}
