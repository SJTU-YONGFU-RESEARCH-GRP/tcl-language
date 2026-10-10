# 10_merge_kit.tcl — Week 27 Day 5 project: stitch a small kit + report
# Run: make week27-10
#      ./scripts/run_calibre_tcl.sh lessons/27/10_merge_kit.tcl
# Writes: tmp/week27_kit.gds , tmp/week27_report.txt

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir

proc write_block {path cell x0 y0 x1 y1} {
    set L [layout create]
    $L units microns 1000
    $L create cell $cell
    $L create layer 1
    $L create polygon $cell 1_0 $x0 $y0 $x1 $y1
    $L gdsout $path $cell
}

set a [file join $outDir week27_kit_a.gds]
set b [file join $outDir week27_kit_b.gds]
set kit [file join $outDir week27_kit.gds]
set report [file join $outDir week27_report.txt]

write_block $a BLOCK_A 0 0 10 10
write_block $b BLOCK_B 0 0 6 6

file delete -force $kit
layout filemerge \
    -infile [list -name $a -placecell [list -refcell BLOCK_A -x 0  -y 0]] \
    -infile [list -name $b -placecell [list -refcell BLOCK_B -x 40 -y 0]] \
    -out $kit \
    -createtop KIT

set M [layout create $kit -dt_expand]

# Also demo import layout into a fresh memory layout
set src [layout create $a -dt_expand]
set L [layout create]
$L import layout $src 0 append

set lines {}
lappend lines "Week 27 merge kit report"
lappend lines "========================"
lappend lines "filemerge -> $kit"
lappend lines "  cells      = [$M cells]"
lappend lines "  children   = [$M children KIT]"
lappend lines "  refs       = [$M iterator ref KIT range 0 end]"
lappend lines "import layout demo (memory)"
lappend lines "  L cells    = [$L cells]"
lappend lines "========================"
lappend lines "Done."

set fh [open $report w]
puts $fh [join $lines \n]
close $fh

puts "Kit GDS: $kit"
puts "Report:  $report"
foreach line $lines { puts $line }
exit
