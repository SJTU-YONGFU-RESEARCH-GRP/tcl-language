# 07_flatten_ref_same.tcl — Week 26 Day 4: flatten ref ≈ expand ref here
# Run: make week26-07
#      ./scripts/run_calibre_tcl.sh lessons/26/07_flatten_ref_same.tcl

proc build {} {
    set L [layout create]
    $L create cell BOX
    $L create layer 1
    $L create polygon BOX 1_0 0 0 10 10
    $L create cell TOP
    $L create ref TOP BOX 0 0 0 0 1
    return $L
}

set L1 [build]
$L1 expand ref TOP BOX 0 0 0 0 1
puts "expand ref  -> n_refs=[llength [$L1 iterator ref TOP range 0 end]] n_poly=[llength [$L1 iterator poly TOP 1 range 0 end]]"

set L2 [build]
$L2 flatten ref TOP BOX 0 0 0 0 1
puts "flatten ref -> n_refs=[llength [$L2 iterator ref TOP range 0 end]] n_poly=[llength [$L2 iterator poly TOP 1 range 0 end]]"

puts "On this machine both leave 0 refs and 1 polygon on TOP."
exit
