set subtotal 80
set threshold 80
if {$subtotal >= $threshold} {
    set shipping 0
} else {
    set shipping 6
}
puts "运费：$shipping"
