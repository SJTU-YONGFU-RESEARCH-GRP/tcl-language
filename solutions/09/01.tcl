set line {temp=24}
set value ""
set matched [regexp {^temp=([0-9]+)$} $line whole value]
puts "匹配：$matched，温度：$value"
