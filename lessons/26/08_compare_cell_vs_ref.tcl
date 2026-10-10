# 08_compare_cell_vs_ref.tcl — Week 26: flatten cell vs expand one ref
# Run: make week26-08
#      ./scripts/run_calibre_tcl.sh lessons/26/08_compare_cell_vs_ref.tcl

proc build_two_refs {} {
    set L [layout create]
    $L create cell BOX
    $L create layer 1
    $L create polygon BOX 1_0 0 0 10 10
    $L create cell TOP
    $L create ref TOP BOX 0 0 0 0 1
    $L create ref TOP BOX 20 0 0 0 1
    return $L
}

set A [build_two_refs]
$A flatten cell TOP
puts "flatten cell TOP:"
puts "  n_refs=[llength [$A iterator ref TOP range 0 end]] n_poly=[llength [$A iterator poly TOP 1 range 0 end]]"

set B [build_two_refs]
$B expand ref TOP BOX 0 0 0 0 1
puts "expand ref (0,0) only:"
puts "  n_refs=[llength [$B iterator ref TOP range 0 end]] n_poly=[llength [$B iterator poly TOP 1 range 0 end]]"

puts "Rule: flatten cell = all instances; expand/flatten ref = one matching instance."
exit
