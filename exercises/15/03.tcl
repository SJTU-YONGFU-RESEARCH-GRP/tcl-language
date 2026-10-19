oo::class create StatsMeter {
    # 完成 constructor、add、average、reset
}
set meter [StatsMeter new]
$meter add 2
$meter add 6
puts [$meter average]
$meter reset
puts [$meter average]
$meter destroy
