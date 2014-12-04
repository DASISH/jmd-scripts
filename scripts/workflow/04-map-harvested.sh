#!/bin/bash

# Traverse the the harvested files and map them. Like the other scripts comprising the workflow, it assumes a structure beneath the data dir: 01-harvested in which each group is represented by a directory in which all the formats harvested from the groups are listed. In every format directory, there is a list of endpoints that provided exactly that format. Finally, in every endpoint directory, it can encounter files harvested.

# On mapping, the records end up in a structure similar to that in 01-harvested. This structure begins with 02-mapped and follows the same form, except that the format directory level is missing. Since the files are mapped, there is no need for that any more. The second difference is that, for each endpoint, the records are stored in a directory called 'json', referring to the format the mapped records are in.

# begin by getting the groups harvested
groups=`echo ${JMDDataDir}/01-harvested/*`
for group in $groups; do
  # remove path, group is defined by the last element
  group=$(basename $group)
  # get formats harvested
  formats=${JMDDataDir}/01-harvested/${group}/results/*
  for format in $formats; do
    # remove path, format is defined by the last element
    format=$(basename $format)
    if [ "$(ls -A ${JMDDataDir}/01-harvested/$group/results/$format)" ]; then
      # directory is not empty
      echo "processing $group" "group, format" $format
      for endpointDir in ${JMDDataDir}/01-harvested/$group/results/$format/*; do
	# get endpoint
	endpoint=`echo $endpointDir | sed 's/.*\\///'`
	echo "processing endpoint" $endpoint
	# if it does not exist, create directory with mapped records
	mappedDir=/home/work/work/02-mapped/$group/$endpoint
	if [ ! -d $mappedDir ]; then
	  mkdir -p $mappedDir
	fi
	# do the mapping
	run-mapper.sh mapfile=$MappingDir/mapfiles/$format.xml inputdir=$endpointDir outputdir=$mappedDir
      done
    fi
  done
done