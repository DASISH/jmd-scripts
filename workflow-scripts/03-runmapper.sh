#!/bin/bash


cd /home/work/work/01-harvested
groups=`echo *`
for group in $groups ; do
    cd $group/results
    formats=`echo *`
    cd -

    for fmt in $formats; do
	# Ensure directory is non-empty.
	if [ "$(ls -A /home/work/work/01-harvested/$group/results/$fmt)" ]; then
	    for x in /home/work/work/01-harvested/$group/results/$fmt/*; do
		y=`echo $x | sed 's/.*\\///'`
		echo y $y
		z=/home/work/work/02-mapped/$group/$y
		if [ ! -d $z ]; then
		    mkdir -p $z
		fi
		cd /home/work/apps/mapper/mapper/current
		./run-mapper.sh mapfile=mapfiles/$fmt.xml inputdir=$x outputdir=$z
		cd -
	    done
	fi
    done
done
