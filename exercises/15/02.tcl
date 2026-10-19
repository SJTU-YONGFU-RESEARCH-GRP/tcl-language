oo::class create SampleMeter {
    # readings 是对象状态
}
set meter [SampleMeter new]
$meter add 5
$meter add 7
puts [$meter values]
$meter destroy
