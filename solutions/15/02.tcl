oo::class create SampleMeter {
    variable readings
    constructor {} { set readings {} }
    method add {value} {
        lappend readings $value
        return [llength $readings]
    }
    method values {} { return $readings }
}
set meter [SampleMeter new]
$meter add 5
$meter add 7
puts [$meter values]
$meter destroy
