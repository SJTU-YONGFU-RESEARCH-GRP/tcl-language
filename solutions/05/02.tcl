set readings {7 -1 0 9 -2}
set emptyReadings {}
set total 0
set count 0
foreach value $readings {
    if {$value < 0} {continue}
    set total [expr {$total + $value}]
    incr count
}
set emptyTotal 0
set emptyCount 0
foreach value $emptyReadings {
    if {$value < 0} {continue}
    set emptyTotal [expr {$emptyTotal + $value}]
    incr emptyCount
}
puts "有效：$count，总和：$total"
puts "空组：$emptyCount，总和：$emptyTotal"
