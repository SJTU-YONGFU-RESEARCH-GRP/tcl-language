array set temperatures {roomA 22 roomB 25}
set temperatures(roomA) 23
foreach key [lsort [array names temperatures]] {
    puts "$key：$temperatures($key)"
}
set snapshot [array get temperatures]
dict set snapshot roomB 26
puts "快照 roomB：[dict get $snapshot roomB]"
