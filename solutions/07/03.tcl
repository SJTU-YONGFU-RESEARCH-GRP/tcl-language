set contacts [list " A@EXAMPLE.ORG " "B@other.org" "   " "c@example.org"]
 set selected {}
 foreach raw $contacts {
     set email [string tolower [string trim $raw]]
     if {$email eq ""} {continue}
     if {[string match {*@example.org} $email]} {
         lappend selected $email
     }
 }
 puts [join $selected "\n"]
 puts "数量：[llength $selected]"
