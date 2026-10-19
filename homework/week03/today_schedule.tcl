# Week 3: list construction, indexing, counting, and appending.
# Run: tclsh homework/week03/today_schedule.tcl

# This is an example Monday study plan, not an official timetable.
set dayName "Monday"
set schedule [list \
    "VLSI Design reading" \
    "Digital circuit exercises" \
    "Semiconductor device review" \
    "Tcl syntax practice" \
    "EDA flow study" \
    "Research paper reading"]

# Add one bonus session after the six-session list is created.
lappend schedule "Weekly study review"
set totalSessions [llength $schedule]

# Human period 4 corresponds to Tcl index 3 (indexing starts at 0).
set period 4
set subject [lindex $schedule [expr {$period - 1}]]

# Print each session manually; loops are introduced in Week 4.
puts "============================================================"
puts "Example study schedule: $dayName"
puts "Full list: $schedule"
puts "Total: $totalSessions periods"
puts "------------------------------------------------------------"
puts "Period 1: [lindex $schedule 0]"
puts "Period 2: [lindex $schedule 1]"
puts "Period 3: [lindex $schedule 2]"
puts "Period 4: [lindex $schedule 3]"
puts "Period 5: [lindex $schedule 4]"
puts "Period 6: [lindex $schedule 5]"
puts "Bonus   : [lindex $schedule 6]"
puts "Selected period $period: $subject"
puts "============================================================"
