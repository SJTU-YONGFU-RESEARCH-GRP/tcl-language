set first [dict create id A]
 set second [dict create id B owner ""]
 set third [dict create id C owner "周 月"]
 set notices {}
 foreach record [list $first $second $third] {
     if {![dict exists $record owner]} {
         lappend notices "未登记"
     } elseif {[dict get $record owner] eq ""} {
         lappend notices "已留空"
     } else {
         lappend notices [dict get $record owner]
     }
 }
 puts [join $notices "\n"]
