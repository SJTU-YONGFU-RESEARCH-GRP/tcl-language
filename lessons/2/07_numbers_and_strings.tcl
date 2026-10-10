# 07_numbers_and_strings.tcl — Week 2: numbers vs text in variables
# Run: make week2-07
#      tclsh lessons/2/07_numbers_and_strings.tcl

# Text goes in quotes
set subject "Math"

# Numbers can be stored without quotes (still a value in a box)
set score 92
set bonus 3

puts "Subject: $subject"
puts "Score  : $score"

# To add numbers, use expr — putting $score and $bonus in quotes would be wrong for math
set total [expr {$score + $bonus}]
puts "Score + bonus = $total"
