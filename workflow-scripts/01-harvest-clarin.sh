#!/bin/bash

export LOGSUFFIX=clarin
cd /home/work/apps/harvester
./run-harvester.sh harvester-config-clarin.xml

../util-scripts/findMapping.sh -i /home/work/work/01-harvested/clarin/results/cmdi/ -d ../../md-mapping/mapfiles/cmdi_template.xml -o ./../md-mapping/mapfiles/cmdi.xml -p /tmp/clarin-profiles


