# 10_report_card.tcl — Week 2 Day 5 project: report card with total
# Run: make week2-10
#      tclsh lessons/2/10_report_card.tcl
# Challenge: change name and scores to yours.

set studentName "Amy"
set school "Sunny Elementary"

set mathScore 88
set englishScore 92
set scienceScore 85

set total [expr {$mathScore + $englishScore + $scienceScore}]

puts "================================"
puts "         REPORT CARD"
puts "================================"
puts "Student : $studentName"
puts "School  : $school"
puts "--------------------------------"
puts "Math    : $mathScore"
puts "English : $englishScore"
puts "Science : $scienceScore"
puts "--------------------------------"
puts "Total   : $total"
puts "================================"
