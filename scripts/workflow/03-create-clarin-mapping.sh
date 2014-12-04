#!/bin/bash

# Generate profile based mappings for the CLARIN harvest. Since the profiles are referred to in the harvested files, these mappings need to be generated after the files have been harvested. Once created, the mappings are added to the directory in which all the mappings reside.

findMapping.sh -i $JMDDataDir/clarin/results/cmdi/ -d ${MappingDir}/mapfiles/cmdi_template.xml -o ${MappingDir}/mapfiles/cmdi.xml -p ${JMDTempDir}/clarin-profiles