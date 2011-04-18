#!/bin/bash 
function replace {
	t="_TEMP"
	newfile="$3$t" 
	sudo cp -R --preserve $3 $newfile
	sed -e "s|$1|$2|g" $newfile > $3
	sudo rm $newfile	
}

replace "188365901207571" "7e57267b847f9d41b751729de713c437" fbcon/templates/base.html
replace "188365901207571" "7e57267b847f9d41b751729de713c437" settings.py


replace "f09191489ff3faff4d3c056838f6339b" "2ddc1db4818c80c38ebf4f9e300c0250" settings.py
