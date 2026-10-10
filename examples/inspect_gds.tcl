set gds [lindex $argv 0]
if {$gds eq ""} {
  set gds [file normalize [file join [file dirname [info script]] .. tmp demo_box.gds]]
}
puts "opening $gds"
set L [layout create $gds]
puts "L=$L"
# list cells via exists / iterator
set r [catch {$L iterator cell} e]
puts "iterator cell: $e"
set r [catch {
  set it [$L iterator cell]
  puts "it=$it"
} e]
puts "e=$e"
# try peek usage
catch {puts [$L exists cell TOP]}
catch {$L iterator} e; puts "iterator bare: $e"
exit
