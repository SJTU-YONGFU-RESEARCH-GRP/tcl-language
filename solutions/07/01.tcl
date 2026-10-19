set raw "  USER.ONE@EXAMPLE.ORG  "
set email [string tolower [string trim $raw]]
set size [string length $email]
set matched [string match {*@example.org} $email]
puts $email
puts "$size $matched"
