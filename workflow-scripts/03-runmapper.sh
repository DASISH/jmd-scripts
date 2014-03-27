#!/bin/bash

cd /home/work/work/01-harvested/results
formats=`echo *`
cd -

for fmt in $formats; do
    # Ensure directory is non-empty.
    if [ "$(ls -A /home/work/work/01-harvested/results/$fmt)" ]; then
	for x in /home/work/work/01-harvested/results/$fmt/*; do
	    y=`echo $x | sed 's/.*\\///'`
	    echo y $y
	    z=/home/work/work/02-mapped/$y
	    if [ ! -d $z ]; then
		mkdir $z
	    fi
	    cd /home/work/apps/mapper/mapper/current
	    ./run-mapper.sh mapfile=mapfiles/$fmt.xml inputdir=$x outputdir=$z
	done
    fi
done
