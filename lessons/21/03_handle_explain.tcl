# 03_handle_explain.tcl — Week 21: what is a handle?
# Run: make week21-03
#      ./scripts/run_calibre_tcl.sh lessons/21/03_handle_explain.tcl
#
# Handle = ticket / name tag for a layout object.
# You store it in a variable, then talk to the layout with $L method ...

set L [layout create]

puts "=== Handle demo ==="
puts "Step 1: layout create  ->  Calibre makes a layout object"
puts "Step 2: set L ...       ->  Tcl stores the handle in L"
puts "Step 3: \$L ...         ->  You call methods on that object"
puts ""
puts "This layout handle is: $L"
puts "Write this in your notebook: handle = $L"

exit
