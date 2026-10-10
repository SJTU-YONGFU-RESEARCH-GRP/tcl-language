set L [layout create]
puts "L=$L"

# Discover subcommands by trying common names / usage errors
foreach m {
  create delete cell layer polygon path wire text rectangle
  gdsout oasis iterator iterator2 peek exists
  createcell createlayer createpolygon
} {
  set r [catch {$L $m} e]
  puts "\$L $m -> rc=$r e=[string range $e 0 200]"
}

puts ----
# Usage dumps
foreach m {create delete gdsout oasis} {
  set r [catch {$L $m -h} e]
  puts "\$L $m -h -> $e"
  set r [catch {$L $m} e]
  puts "\$L $m -> $e"
}

puts ----
# Build a tiny chip: cell + layer + polygon + gdsout
set r [catch {$L create cell TOP} e]; puts "create cell: $r $e"
set r [catch {$L create layer 1} e]; puts "create layer: $r $e"
set r [catch {$L create layer 1 name METAL1} e]; puts "create layer named: $r $e"
set r [catch {$L create polygon TOP 1 {0 0 10 0 10 10 0 10}} e]; puts "polygon: $r $e"
set r [catch {$L create rectangle TOP 1 0 0 10 10} e]; puts "rectangle: $r $e"

set out /home/yongfu/proj/tcl-language/tmp/demo.gds
file mkdir [file dirname $out]
set r [catch {$L gdsout $out} e]; puts "gdsout: $r $e"
puts "exists out? [file exists $out] size=[expr {[file exists $out] ? [file size $out] : 0}]"

# reopen
set r [catch {set L2 [layout create $out]} e]; puts "reopen create file: $r $e"
set r [catch {open $out} e]; puts "open cmd: $r $e"

exit
