#!/bin/bash

LOGSUFFIX=dariah
export LOGSUFFIX
# harvester will use variable for logging

# define output dir in harvester configuration file

# invoke the harvester, pass the cessda configuration to it
run-harvester.sh $JMDConfDir/harvester/harvester-config-dariah.xml