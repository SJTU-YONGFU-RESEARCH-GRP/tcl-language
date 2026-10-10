# show_tcl_help.tcl — print Tcl commands useful for learning (run with tclsh)
# Usage: tclsh tools/show_tcl_help.tcl
#        make help-tcl

puts "=== Tcl learning commands (tclsh) ==="
puts "Tcl version: $tcl_version"
puts ""

set groups {
    {Week 1-2 basics} {puts set expr exit catch}
    {Week 3 lists} {list lindex llength lappend lsort lrange}
    {Week 4 control} {if foreach for while break continue incr}
    {Week 5 procs/files} {proc return open close gets file}
    {Week 6 OOP} {oo::class create oo::define oo::objdefine}
    {Discovery} {info unknown auto_load}
}

foreach {title cmds} $groups {
    puts "--- $title ---"
    foreach c $cmds {
        if {[info commands $c] ne ""} {
            puts "  $c"
        } else {
            puts "  $c (not loaded — need package or Tcl 8.6+)"
        }
    }
    puts ""
}

puts "=== How to learn a command (no built-in help) ==="
puts "1. Typo on purpose: tclsh -> type 'setx' -> read 'invalid command name'"
puts "2. man page:   man 3 puts   (Linux, if tk/doc installed)"
puts "3. Online:     https://www.tcl-lang.org/man/tcl8.6/TclCmd/contents.htm"
puts "4. In script:  catch {badcommand} msg ; puts \$msg"
puts ""
puts "=== info subcommands (try in tclsh) ==="
puts "  info commands    — list command names"
puts "  info vars        — list global variables"
puts "  info script      — current script file"
puts "  info exists x    — does variable x exist?"
puts ""
