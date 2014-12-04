
#!/bin/bash

# Traverse the the harmonized files, and append them to one single file. The reason for this is that uploading this file requires less time than uploading each and every json file separately. This script assumes the 03-harmonized structure described in harmonize map script.

python make-jsonl.py -i ${JMDDataDir}/03-harmonized -o ${JMDDataDir}/data2upload.jsonl
