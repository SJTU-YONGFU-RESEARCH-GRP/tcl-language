# 10_my_hello_layout.tcl — Week 21 Day 5 project: intro + empty layout + handle
# Run: make week21-10
#      ./scripts/run_calibre_tcl.sh lessons/21/10_my_hello_layout.tcl
# Challenge: change name and add one comment about handles.

set studentName "Amy"
set goal "Learn Calibre layout handles"

puts "================================"
puts "   MY CALIBRE HELLO SCRIPT"
puts "================================"
puts "Name : $studentName"
puts "Goal : $goal"
puts "--------------------------------"

set L [layout create]
$L create cell TOP

puts "I created an empty layout."
puts "Handle L = $L"
puts "I also created cell TOP on this layout."
puts "================================"

exit
