set price 25
set quantity 3
set discount 10
set emptyQuantity 0
set payable [expr {$price * $quantity - $discount}]
set emptyPayable [expr {$price * $emptyQuantity}]
puts "应付：$payable"
puts "空单：$emptyPayable"
