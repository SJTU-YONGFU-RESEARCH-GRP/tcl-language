# 06_oop_comparison.tcl — Week 7 Day 4: Pet new vs layout create
# Run: make week7-06
#      ./scripts/run_calibre_tcl.sh lessons/7/06_oop_comparison.tcl
#
# Week 6 OOP          |  Week 7 Calibre
# --------------------|------------------
# Pet new             |  layout create
# $cat speak          |  $L create cell TOP
# method on object    |  method on layout handle

puts "=== OOP glasses for Calibre ==="
puts "Pet new          <->  layout create"
puts "\$cat speak       <->  \$L create cell TOP"
puts "object.method    <->  \$L gdsout ..."
puts ""

set L [layout create]
puts "Created layout handle: $L"
$L create cell TOP
puts "Called: \$L create cell TOP"
puts "Same pattern as Week 6 — different API."

exit
