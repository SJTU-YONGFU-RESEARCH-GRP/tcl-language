# 10_string_toolkit.tcl — Week 6 Day 5 project: clean and summarize a line
# Run: make week6-10
# Writes: tmp/week6_toolkit.txt

set repoRoot [file normalize [file join [file dirname [info script]] ../..]]
set outDir [file join $repoRoot tmp]
file mkdir $outDir
set out [file join $outDir week6_toolkit.txt]

set raw "   Hello, Tcl STRING toolkit!!!   "
set clean [string trim $raw]
set lower [string tolower $clean]
set title [string totitle $lower]
set starred [string map {{!!!} {!} {,} {}} $title]
set summary [string cat "len=" [string length $clean] " first=" [string index $clean 0]]

set lines [list \
    "Week 6 string toolkit" \
    "======================" \
    "raw     = <$raw>" \
    "trim    = <$clean>" \
    "lower   = $lower" \
    "title   = $title" \
    "mapped  = $starred" \
    "summary = $summary" \
    "match Hello* ? [string match {Hello*} $clean]" \
    "======================" \
    "Done."]

set fh [open $out w]
puts $fh [join $lines \n]
close $fh

puts "Wrote $out"
foreach line $lines { puts $line }
exit
