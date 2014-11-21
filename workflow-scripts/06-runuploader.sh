#!/bin/bash

# change parameters as needed, this is just an example
numberOfprocesses=4
apiKey=fb5734f2-7153-4efc-ac41-e532e38d9fca
url=http://tlatest02.mpi.nl
data2upload=/home/work/data2upload.jsonl


# uncomment for url-based uploading
#ckanapi load datasets -I $data2upload -p $numberOfprocesses -r $url -a $apiKey

# comment for url-based uploading
configFile=/etc/ckan/default/development.ini
ckanapi load datasets -I $data2upload -p $numberOfprocesses -c $configFile
