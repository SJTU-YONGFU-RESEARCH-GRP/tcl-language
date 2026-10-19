set items [list 资料包 "A*组" A1组]
set targetIndex [lsearch -exact $items "A*组"]
set missingIndex [lsearch -exact $items B组]
set tail [lrange $items 1 end]
puts "$targetIndex $missingIndex"
puts [join $tail " / "]
