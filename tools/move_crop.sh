#!/bin/bash
#
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
            prex=${file:0:7}
            if [ "$prex" == "Cropped" ]
            then
                `cp $path /share/front/cropped_data/`
            fi
		fi
		done
}
IFS=$'\n'
INIT_PATH="/share/front/yellow"
ergodic $INIT_PATH

#file='Cropped_a010b01c01d02e02_image.jpg'
#prex='Cropped'
#prefile=${file:0:7}
#if [ "$prefile" == "Croppe" ]
#then
#    echo "ok"
#fi
