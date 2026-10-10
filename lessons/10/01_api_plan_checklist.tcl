# 01_api_plan_checklist.tcl — Week 10 Day 1: plan which APIs you will use
# Run: make week10-01
#      ./scripts/run_calibre_tcl.sh lessons/10/01_api_plan_checklist.tcl

puts "Week 10 graduation — API plan"
puts "=============================="
puts "Create:"
puts {[ ] layout create}
puts {[ ] $L create cell}
puts {[ ] $L create layer}
puts "Geometry:"
puts {[ ] $L create polygon}
puts {[ ] $L create text}
puts {[ ] $L create wire   (optional)}
puts "Hierarchy:"
puts {[ ] $L create ref}
puts "Query / export:"
puts {[ ] $L gdsout}
puts {[ ] layout peek / $L cells / $L bbox}
puts "=============================="
puts "Pick a project: house / brick array / letter / OOP factory"
exit
