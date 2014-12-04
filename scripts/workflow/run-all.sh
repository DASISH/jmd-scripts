#!/bin/bash

echo "### Step 1: Harvest metadata ###"
echo "--------------------------------"
./01-harvest.sh > logs/01-harv.txt

echo "### Step 2: Update the mapper from svn (if necessary) ###"
echo "---------------------------------------------------------"
./02-updatemapper.sh > logs/02-upd.txt

echo "### Step 3: Run mapper on harvested records ###"
echo "-----------------------------------------------"
./03-runmapper.sh > logs/03-map.txt

echo "### Step 4: Upload mapped records ###"
echo "-------------------------------------"
for x in /home/work/work/02-mapped/*; do
    y=`echo $x | sed 's/.*\\///'`
    ./04-upload.sh $x/json $y
done
