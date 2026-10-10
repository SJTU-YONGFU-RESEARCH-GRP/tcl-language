# 11_two_layouts_two_handles.tcl — Week 7 bonus: two handles, two layouts
# Run: make week7-11
#      ./scripts/run_calibre_tcl.sh lessons/7/11_two_layouts_two_handles.tcl

set L1 [layout create]
set L2 [layout create]

$L1 create cell TOP
$L2 create cell CHIP

puts "First layout  handle: $L1  (cell TOP)"
puts "Second layout handle: $L2  (cell CHIP)"
puts "Two molds, two toys — like two Pet objects in Week 6."

exit
