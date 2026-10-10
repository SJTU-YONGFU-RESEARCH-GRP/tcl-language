# 09_file_exists_size.tcl — Week 5: file exists and file size
# Run: make week5-09
#      tclsh lessons/5/09_file_exists_size.tcl

file mkdir tmp

set path tmp/week5_diary.txt

if {[file exists $path]} {
    set bytes [file size $path]
    puts "File exists: $path"
    puts "Size: $bytes bytes"
} else {
    puts "File not found: $path"
    puts "Run make week5-05 first, or this file will appear after week5 runs."
}

set dir tmp
if {![file exists $dir]} {
    file mkdir $dir
    puts "Created directory $dir"
} else {
    puts "Directory $dir is ready."
}
