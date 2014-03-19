jmd-scripts
===========

This repository contains scripts and documentation relevant to the
workflow of the Joint Metadata Domain (task 5.4). The intention is
that eventually the documentation here would be sufficient to
replicate the implementation completely. (We're not quite there
yet...)

The JMD's workflow comprises three stages:

1. Fetching of original metadata records with **OAI-PMH harvesting**.
2. Performing **semantic mappings** into the JMD's internal
representation.
3. Ingestion of metadata into, and other setup related to, the **web
portal**.

Between stages, the metadata is stored on the file system to minimise
interdependency between the stages.


## Harvesting

OAI-PMH harvesting is a well defined process, so this part is
straightforward. We use our [OAI Harvest
Manager](https://github.com/TheLanguageArchive/oai-harvest-manager)
for it. See the [configuration file](harvester-config.xml) for
details. One thing of note is that formats to be harvested are mostly
defined based on the metadata schema (in which case, the harvester
performs a ````ListMetadataFormats```` query and harvests using all
metadata prefixes that fit the specified schema).

## Mapping

The mappings are stored and documented in a [separate
repository](https://github.com/DASISH/md-mapping).

## Web portal

The current implementation is based on [CKAN](http://ckan.org/), but
it could equally be built on top of other Solr based systems. Some
performance tweaks are used, which will be documented here.
