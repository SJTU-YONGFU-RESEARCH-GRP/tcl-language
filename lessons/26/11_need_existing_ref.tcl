# 11_need_existing_ref.tcl — Week 26 bonus: expand ref needs a matching sref
# Run: make week26-11
#      ./scripts/run_calibre_tcl.sh lessons/26/11_need_existing_ref.tcl

set L [layout create]
$L create cell BOX
$L create layer 1
$L create polygon BOX 1_0 0 0 10 10
$L create cell TOP
# Intentionally NO create ref

puts "Calling expand ref without create ref first..."
if {[catch {$L expand ref TOP BOX 0 0 0 0 1} err]} {
    puts "Caught error (expected):"
    puts "  $err"
} else {
    puts "Unexpected success"
}

puts ""
puts "Fix: \$L create ref TOP BOX 0 0 0 0 1   then   \$L expand ref TOP BOX 0 0 0 0 1"
exit
