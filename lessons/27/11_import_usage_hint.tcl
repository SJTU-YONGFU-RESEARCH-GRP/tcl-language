# 11_import_usage_hint.tcl — Week 27: Usage + wrong arity
# Run: make week27-11
#      ./scripts/run_calibre_tcl.sh lessons/27/11_import_usage_hint.tcl

set L [layout create]
set S [layout create]
$S create cell X
$S create layer 1
$S create polygon X 1_0 0 0 1 1

puts "=== incomplete import layout ==="
if {[catch {$L import layout} msg]} {
    puts $msg
}

puts ""
puts "=== missing mode (needs append|overwrite|rename) ==="
if {[catch {$L import layout $S 0 0} msg]} {
    puts $msg
}

puts ""
puts "Correct:  \$L import layout \$src 0 append"
exit
