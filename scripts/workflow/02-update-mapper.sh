#!/bin/bash

# Update the mapper and mappings. The update-deploy script does this by querying both the GitHub repository for the mapper and the one for the DASISH mappings. For more information, please refer to

# https://github.com/DASISH/md-mapping

# Please note that the updating is done from the directory in which the mapper sources are located. When updating, the update and deploy script will create, at the same directory level, a target directory in which the application and the mapping definitions are deployed. From this directory the actual mapping will be carried out. So if the directory we are in now is

# /a/b/md-mapper

# the script will create

# /a/b/mapper

cd $MapperSourceDir
./update-deploy.pl

# Now the MapperDir (refer to the SetJMDContext script) will hold up to date an up to date mapper and mapping definitions to carry out the mapping

# Important note: when the update and deploy script is invoked for the first time, it needs the -f switch. Otherwise the

# /a/b/mapper

# directory will not be created.