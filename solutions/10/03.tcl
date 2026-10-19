set subtotal 88
proc orderFee {count price {delivery 0} {rate 1.0}} {
    set subtotal [expr {$count * $price}]
    return [expr {$subtotal * $rate + $delivery}]
}
puts [format "%.2f" [orderFee 2 15 5 0.8]]
puts "外部 subtotal：$subtotal"
