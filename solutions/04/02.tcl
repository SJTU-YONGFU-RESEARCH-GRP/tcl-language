set value 35
if {$value < 10} {
    set label "偏低"
} elseif {$value <= 30} {
    set label "正常"
} else {
    set label "偏高"
}
puts $label
