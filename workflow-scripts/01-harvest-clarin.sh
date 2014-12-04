#!/bin/bash

export LOGSUFFIX=clarin
cd /home/work/apps/harvester
./run-harvester.sh harvester-config-clarin.xml

input=/home/work/work/01-harvested/clarin/results/cmdi/
template=/home/work/apps/mapper/md-mapping/mapfiles/cmdi_template.xml
output=/home/work/apps/mapper/md-mapping/mapfiles/cmdi.xml

/home/work/jmd-scripts/util-scripts/findMapping.sh -i $input -d $template -o $output  -p /tmp/clarin-profiles


