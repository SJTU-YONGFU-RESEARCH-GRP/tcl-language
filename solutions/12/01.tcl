proc requireCount {text} {
    if {![string is integer -strict $text] || $text < 0} {
        error "人数必须是非负整数"
    }
    return $text
}
puts [requireCount 0]
if {[catch {requireCount -2} message]} { puts $message }
