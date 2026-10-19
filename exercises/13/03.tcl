set total 500
namespace eval budget {
    variable total 0
    # 定义 add、get 和 reset
}
puts [::budget::add 6]
puts [::budget::add 9]
puts "外部：$total"
puts "清零：[::budget::reset]"
