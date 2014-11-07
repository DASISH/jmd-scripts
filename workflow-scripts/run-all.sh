
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

echo "### Step 4: Run harmonizer on mapped records ###"
echo "-----------------------------------------------"
./04-runharmonizer.sh > logs/04-harmonize.tx 

echo "### Step 5: Run make-jsonline on harmonized records ###"
echo "-----------------------------------------------"
./05-runmake-jsonl.sh > logs/05-jsonline.tx 

echo "### Step 6: Upload records ###"
echo "-------------------------------------"
./06-runuploader.sh > logs/06-upload.txt
