oo::class create NamedMeter {
    # 声明对象变量，定义构造器与 label 方法
}
set meter [NamedMeter new {温度计 A}]
puts [$meter label]
$meter destroy
