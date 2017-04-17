set logfile [open "convert.log" w]
set word_file [glob "input/*jpg"] 
set out_dir processed
foreach var $word_file {
	puts $var
	if {[file exists $var] == 0} {
		puts "Error : $var - file not found"
		puts $logfile "Error : $var - file not found"
		continue
	}
	set out [lindex [split $var "/"] 1] 
	puts $out
	exec convert -crop +871+380 -crop -469-768 +repage "$var" "$out_dir/$out"
}
