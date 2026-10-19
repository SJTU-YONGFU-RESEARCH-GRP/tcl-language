proc stationeryFee {count unitPrice} {
    return [expr {$count * $unitPrice}]
}
puts [stationeryFee 4 3]
puts [stationeryFee 2 7]
