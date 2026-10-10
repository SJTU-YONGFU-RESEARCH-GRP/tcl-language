# Probe Calibre DESIGNrev layout API
puts "tcl_version=$tcl_version"

puts "layout ensemble? [namespace ensemble exists layout]"
if {[namespace ensemble exists layout]} {
  catch {puts "ensemble map: [namespace ensemble configure layout -map]"}
}

foreach c {layout open gdsout oasis cell layer} {
  puts "cmd exists $c? [expr {[llength [info commands $c]] > 0}]"
}

# Try create
set rc [catch {set L [layout create]} err]
puts "layout create rc=$rc L=[info exists L] err=$err"
if {[info exists L]} {
  puts "L='$L'"
  foreach cmd {
    {layout create cell $L TOP}
    {$L create cell TOP}
    {layout cell create $L TOP}
    {setLCV $L TOP}
  } {
    set r [catch {uplevel #0 $cmd} e]
    puts "TRY {$cmd} -> rc=$r e=$e"
  }
}

# Builtin help variants
foreach topic {layout "layout create" open gdsout} {
  set r [catch {help $topic} e]
  puts "help($topic) rc=$r len=[string length $e]"
  if {[string length $e] > 0 && [string length $e] < 2000} {
    puts $e
  }
}

exit
