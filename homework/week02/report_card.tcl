# Week 2: variables, expressions, quoting, and substitution.
# Run: tclsh homework/week02/report_card.tcl

set studentName "GateUltra"
set school "Shanghai Jiao Tong University"

# These courses and scores are example data, not an actual transcript.
set course1 "VLSI Design"
set course2 "Digital Integrated Circuit Design"
set course3 "EDA Design Automation"
set score1 88
set score2 92
set score3 85

# [expr ...] runs a command and substitutes its result into set.
# Braces protect the expression; expr itself evaluates the variables.
set total [expr {$score1 + $score2 + $score3}]
set average [expr {$total / 3}]

# Header: double quotes allow $variable substitution.
puts "============================================================"
puts "Example Course Report - $studentName"
puts "School: $school"
puts "Scores below are example data."
puts "============================================================"

# Scores and results: use variable values instead of fixed totals.
puts "$course1: $score1"
puts "$course2: $score2"
puts "$course3: $score3"
puts "Total: $total"
puts "Average: $average (integer division)"

# Quoting comparison: braces keep $ and [] literal at this stage.
puts "Double quotes: student=$studentName; total=$total"
puts {Braces: student=$studentName; total=[expr {$score1 + $score2 + $score3}]}

# Footer: mark the end of the report.
puts "============================================================"
