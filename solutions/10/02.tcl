proc packedFee {count price {pack 2}} {
    return [expr {$count * $price + $pack}]
}
puts [packedFee 3 4]
puts [packedFee 3 4 0]
