oo::class create NamedMeter {
    variable name
    constructor {label} { set name $label }
    method label {} { return $name }
}
set meter [NamedMeter new {温度计 A}]
puts [$meter label]
$meter destroy
