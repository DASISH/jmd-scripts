
#!/bin/bash

# Traverse the the mapped files and harmonize them. This script assumes the 02-mapped structure described in the mapper script. The harmonizing process creates a directory named 03-harmonized. In it, you will find the same structure as in the 02-mapped directory.

# create the dict directory if it is not there
if [ ! -d "${JMDDataDir}/dict" ]; then
  # the dict directory does not exist; create it
  mkdir "${JMDDataDir}/dict/"
fi

python md-harmonizer.py -i ${JMDDataDir}/02-mapped -c ${JMDConfDir}/harmonizer/harmonizer-config.txt -o ${JMDDataDir}/03-harmonized -d ${JMDDataDir}/dict/ctable.pkl