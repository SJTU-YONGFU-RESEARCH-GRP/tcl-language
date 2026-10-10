# 10_today_schedule.tcl — Week 3 Day 5 project: class schedule
# Run: make week3-10
#      tclsh lessons/3/10_today_schedule.tcl
# Challenge: change subjects and which period you print.

set dayName "Monday"
set schedule [list Math English Science Art Tcl]

set period 3
set subject [lindex $schedule [expr {$period - 1}]]

set totalClasses [llength $schedule]

puts "================================"
puts "     TODAY'S CLASS SCHEDULE"
puts "================================"
puts "Day     : $dayName"
puts "Classes : $schedule"
puts "Total   : $totalClasses periods"
puts "--------------------------------"
puts "Period 1 : [lindex $schedule 0]"
puts "Period 2 : [lindex $schedule 1]"
puts "Period 3 : [lindex $schedule 2]"
puts "Period 4 : [lindex $schedule 3]"
puts "Period 5 : [lindex $schedule 4]"
puts "--------------------------------"
puts "Highlight: Period $period is $subject"
puts "================================"
