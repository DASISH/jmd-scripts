#!/bin/bash

# Traverse the the harmonized files, and append them to one single file. The reason for this is that uploading this file requires less time than uploading each and every json file separately. This script assumes the 03-harmonized structure described in harmonize map script.

# activate the CKAN virtual environment

cd $CKANvirtualEnvironment
. bin/activate


if [ "z${CKANparallelUploads}" = "z" ]; then
  # parallel uploads not intended, for convenience, use 1
  $CKANparallelUploads=1
fi

if [ "z${CKANurl}" != "z" ]; then
  # A url to the ckan server has been defined. In this case, the CKANapiKey needs to be there as well.
  if [ "z${CKANapiKey}" = "z" ]; then
    # the variable has not been defined, upload is not possible
    echo "CKAN api key has not been defined. This blocks uploading. Note: for local uploading, please remove the definition of the CKANurl variable from the context file."
  else
    # uploading is possible
    ckanapi load datasets -I ${JMDDataDir}/data2upload.jsonl -p $CKANparallelUploads -r $CKANurl -a $CKANapiKey
  fi
else
  # No url defined, assume local upload is intended

  ckanapi load datasets -I ${JMDDataDir}/data2upload.jsonl -p $CKANparallelUploads -c $CKANconfigFile
fi

# deactivate the CKAN virtual environment
# by exiting perhaps