#!/bin/bash
#
#site: www.ahlinux.com
function ergodic(){
	for file in `ls $1`
	do
		if [ -d $1"/"$file ]
		then
			ergodic $1"/"$file
		else
			local path=$1"/"$file 
			local name=$file      
			local size=`du --max-depth=1 $path|awk '{print $1}'` 
#echo $name  $size $path 
			echo $path 
		fi
		done
}
IFS=$'\n'
INIT_PATH="/share/front"
ergodic $INIT_PATH
