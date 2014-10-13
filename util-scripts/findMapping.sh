#!/bin/bash

# Welcome info
show_welcome() {
	cat << EOF
CLARIN Component Metadata facet mapping!
><><><><><><><><><><><><><><><><><><><><
EOF
}

# Usage info
show_help() {
	show_welcome
	cat << EOF
Usage: ${0##*/} [-hv] [-c CLFACET] [-d DASMAP] [-p CACHEDIR] [-r REGURL] [-i INDIR] [-x EXTGLOB] [-o OUTFILE]
Determine the mappings for the CMD records in INDIR and write them to OUTFILE.

    -h          display this help and exit
    -c CLFACET  location of the CLARIN facet mapping (URL)
                (default https://lux17.mpi.nl/isocat/clarin/vlo/mapping/facetConcepts.xml)
    -d DASMAP   location of the DASISH facet mapping file
                (default ./DASISH-mapping.xml)
    -p CACHEDIR location of the CMD profile cache
                (default ./.profile-cache)
    -r REGURL   URL of profiles endpoint of the CLARIN Component Registry
                (default http://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/profiles)
    -i INDIR    examine the records in this directory
                (default .)
    -x EXTGLOB  glob to select the records in the input directory
                (default *.xml)
    -o OUTFILE  put the resulting mapping in this file
                (default ./CLARIN-DASISH-mapping.xml)
    -v          be verbose.
EOF
}

# Initialize our own variables:
clarin_fc="https://lux17.mpi.nl/isocat/clarin/vlo/mapping/facetConcepts.xml"
dasish_fc="./DASISH-mapping.xml"
profile_cache="./.profile-cache"
registry="http://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/profiles"
input_dir="."
ext_glob="*.xml"
output_file="./CLARIN-DASISH-mapping.xml"
verbose=0

OPTIND=1 # Reset
while getopts "h?c:d:p:r:i:x:o:v" opt; do
	case "$opt" in
		h|\?)
			show_help
			exit 0
			;;
		v)
			verbose=1
			;;
		c)
			clarin_fc=$OPTARG
			;;
		d)
			dasish_fc=$OPTARG
			;;
		p)
			profile_cache=$OPTARG
			;;
		r)
			registry=$OPTARG
			;;
		i)
			input_dir=$OPTARG
			;;
		x)
			ext_glob=$OPTARG
			;;
		o)
			output_file=$OPTARG
			;;
		'?')
			show_help >&2
			exit 1
			;;
	esac
done
shift "$((OPTIND-1))" # Shift off the options and optional --.

if [ $verbose -ne 0 ]; then
	show_welcome
	echo "Run: `date`"
	echo "Input directory: $input_dir"
	echo "Number of records: `find $input_dir -type f -name "$ext_glob" | wc -l`"
fi

# @xsi:schemaLocation should be on the root so try to speed up by reading just some top lines from the CMD record
# TODO (?): relace by a streaming xml parser, this is not really a safe way to get the info
profiles="`find $input_dir -type f -name "$ext_glob" -exec head -n 25 {} \; | grep 'schemaLocation' | sed -e 's|.*\(clarin.eu:cr1:p_[0-9]*\).*|\1|g' | sed -e 's|^[^c].*||g' | sort | uniq`"

if [ $verbose -ne 0 ]; then
	echo "Number of profiles: `echo $profiles | wc -w`"
	echo "Profiles: `for p in $profiles; do echo -n "$p ";done`"
fi

if [ $verbose -ne 0 ]; then
	echo "Profile cache: $profile_cache"
fi

if [ ! -d $profile_cache ]; then
	mkdir -p $profile_cache
	if [ $verbose -ne 0 ]; then
		echo "Created profile cache directory"
	fi
else
	rm $profile_cache/*
	if [ $verbose -ne 0 ]; then
		echo "Cleaned profile cache directory"
	fi
fi

if [ $verbose -ne 0 ]; then
	echo "Profile registry: $registry"
fi

for profile in $profiles; do
	if [ ! -f $profile_cache/$profile.xml ]; then
		curl -s -o "$profile_cache/$profile.xml" "$registry/$profile/xml"
		if [ $verbose -ne 0 ]; then
			echo "Fechted profile: $profile from $registry/$profile/xml to $profile_cache/$profile.xml"
		fi
	fi
done

if [ $verbose -ne 0 ]; then
	echo "CLARIN facet mapping: $clarin_fc"
	echo "DASISH facet mapping: $dasish_fc"
fi

${0%%/*}/xsl2 -xsl:${0%%/*}/createMapping.xsl -s:$dasish_fc clarin_fc=$clarin_fc profile_cache=$profile_cache > $output_file

if [ $verbose -ne 0 ]; then
	echo "Output file: $output_file"
	echo "Output mapping:"
	cat $output_file
fi