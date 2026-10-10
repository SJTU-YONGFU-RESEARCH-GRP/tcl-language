# Create TOP cell with a 100x100 box on layer 1 and write GDSII.
# Run:
#   ./run_calibre_tcl.sh examples/create_box.tcl
#
# Then view in VNC GUI:
#   source setup_calibredrv.sh && export DISPLAY=:33
#   calibredrv tmp/demo_box.gds

set outDir [file normalize [file join [file dirname [info script]] .. tmp]]
file mkdir $outDir
set gds [file join $outDir demo_box.gds]

set L [layout create]
$L create cell TOP
$L create layer 1

# polygon: cell L_D  x1 y1 ... xn yn   (L_D = layer_datatype)
$L create polygon TOP 1_0 \
  0 0 \
  100 0 \
  100 100 \
  0 100

puts "Writing $gds"
$L gdsout $gds TOP
puts "done size=[file size $gds] bytes"
exit
