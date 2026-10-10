# 11_compare_all.tcl — Week 28: side-by-side counts for AND/OR/NOT/XOR
# Run: make week28-11
#      ./scripts/run_calibre_tcl.sh lessons/28/11_compare_all.tcl

set L [layout create]
$L units microns 1000
$L create cell TOP
foreach ly {1 2 3 4 5 6} { $L create layer $ly }
$L create polygon TOP 1_0 0 0 20 20
$L create polygon TOP 2_0 10 10 30 30

$L AND 1 2 3
$L OR  1 2 4
$L NOT 1 2 5
$L XOR 1 2 6

puts "Operation  out_layer  npoly"
puts "---------  ---------  -----"
foreach {op ly} {AND 3 OR 4 NOT 5 XOR 6} {
    set n [llength [$L iterator poly TOP $ly range 0 end]]
    puts [format "%-9s  %-9s  %s" $op $ly $n]
}
puts "Rule of thumb: AND=overlap, OR=union, NOT=cut, XOR=only-exclusive"
exit
