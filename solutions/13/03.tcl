set total 500
namespace eval budget {
    variable total 0
    proc add {amount} {
        variable total
        set total [expr {$total + $amount}]
        return $total
    }
    proc get {} {
        variable total
        return $total
    }
    proc reset {} {
        variable total
        set total 0
        return $total
    }
}
puts [::budget::add 6]
puts [::budget::add 9]
puts "外部：$total"
puts "清零：[::budget::reset]"
