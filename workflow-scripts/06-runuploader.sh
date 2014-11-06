#!/bin/bash

# change parameters as needed, this is just an example
numberOfprocesses=4
apiKey=fb5734f2-7153-4efc-ac41-e532e38d9fca
url=http://tlatest02.mpi.nl
data2upload=/home/work/data2upload.jsonl

ckanapi load datasets -I $data2upload -p $numberOfprocesses -r $url -a $apiKey

