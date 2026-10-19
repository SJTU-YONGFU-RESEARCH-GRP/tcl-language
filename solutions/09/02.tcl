set samples [list {temp=-8} {temp=0} {temp=bad}]
set values {}
set rejected {}
foreach line $samples {
    if {[regexp {^temp=(-?[0-9]+)$} $line whole value]} {
        lappend values $value
    } else {
        lappend rejected $line
    }
}
puts "有效：[join $values {, }]"
puts "拒绝：[join $rejected {, }]"
