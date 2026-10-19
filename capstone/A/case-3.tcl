# Execute after the project implementation: 非法列表明确报错
set malformed [format %c 123]
puts "非法列表: [catch {cleanRegistrations $malformed}]"
