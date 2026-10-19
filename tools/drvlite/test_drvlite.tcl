# test_drvlite.tcl — Self-test suite for DRV-Lite simulator

source [file join [file dirname [info script]] "drvlite.tcl"]

puts "\n>>> Testing layout create..."
set L [layout create]
puts "Pass: created layout handle: $L"

puts "\n>>> Testing cell creation..."
$L create cell TOP
$L create cell SUB1
set cells [$L cells]
puts "Pass: cells in layout = $cells"
if {[lsearch $cells "TOP"] == -1 || [lsearch $cells "SUB1"] == -1} {
    error "FAIL: TOP or SUB1 missing from cells"
}

puts "\n>>> Testing polygon creation & bounding box..."
$L create polygon TOP 1 0 0 500 0 500 300 0 300
set bb [$L bbox TOP]
puts "Pass: bounding box of TOP = $bb"
if {$bb ne "0 0 500 300"} {
    error "FAIL: unexpected bbox: $bb (expected: 0 0 500 300)"
}

puts "\n>>> Testing layer tracking..."
set layers [$L layers TOP]
puts "Pass: layers in TOP = $layers"
if {[lsearch $layers 1] == -1} {
    error "FAIL: layer 1 missing"
}

puts "\n>>> Testing layout peek..."
set top [layout peek "my_chip.gds" -topcell]
puts "Pass: peek returned topcell = $top"

puts "\n>>> Testing layout export (gdsout)..."
set tmp_gds [file join [file dirname [info script]] "test_out.gds"]
$L gdsout $tmp_gds TOP
if {[file exists $tmp_gds]} {
    puts "Pass: successfully exported $tmp_gds"
    file delete -force $tmp_gds
} else {
    error "FAIL: output file not created"
}

puts "\n=============================================="
puts " ALL DRV-Lite TESTS PASSED SUCCESSFULLY! (6/6)"
puts "=============================================="
