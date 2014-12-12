#!/bin/bash

# procedure that adds a path not already in PATH
addPath() {
    if [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]]; then
        PATH="${PATH:+"$PATH:"}$1"
    fi
}


# --- general definitions

# directory in which messages are to be logged
JDMLogDir=/home/work/jmd/log
export JDMLogDir

# directory where the JMD scripts are
JMDScriptDir=/home/work/jmd/scripts
export JMDScriptDir

# directory for temporary files
JMDTempDir=/home/work/jmd/temp
export JMDTempDir

# directory where the JMD configuration files are
JMDConfDir=/home/work/jmd/conf
export JMDConfDir


# --- harvest manager related definitions

# directory in which harvester messages are to be logged
#HLOGDIR=$JDMLogDir
#export HLOGDIR
# harvester will use variable for logging
# still needs to be added to the harvester package

# directory into which the harvester is installed
HarvesterDir=/home/work/apps/harvest-manager
export HarvesterDir

# directory where the harvested files are stored
# JMDDataDir=/home/work/jmd/data
# for the moment, use the existing harvest
JMDDataDir=/home/work/work
export JMDDataDir
# note: this directory needs to be referred to in the harvester configuration files


# --- mapper related definitions

# directory into which the mapper is installed
MapperDir=/home/work/apps/mapper/current
export MapperDir


# directory into which the mapper is installed
MapperSourceDir=/home/work/apps/md-mapper
export MapperSourceDir

# directory into which the mappings are stored
MappingDir=/home/work/apps/md-mapping
export MappingDir

MLOGDIR=$JDMLogDir
export MLOGDIR
# mapper will use variable for logging
# still needs to be added to the harvester package
# --- clarin mapping generation

# for clarin, mapping files depend on the profiles used in the data, and therefore need to be generated after harvesting the data

# directory in which the script and definitions needed for this is stored

ClarinMappingDir=/home/work/jmd/scripts/clarin/
export ClarinMappingDir


# --- CKAN related definitions

CKANparallelUploads=4
# CKANapiKey=someKey
# CKANurl=http://127.0.0.1
CKANconfigFile=/etc/ckan/default/production.ini

# Note: only the CKANconfigFile definition is mandatory. If the url will not have been defined, CKAN is assumed to reside locally, and the http interface will not be used for uploading.

CKANvirtualEnvironment=/usr/lib/ckan/default


# --- add the applications used to the path

addPath $HarvesterDir
addPath $MapperDir
addPath $ClarinMappingDir

export PATH

# after this, outside the script, do: source ./SetJMDContext