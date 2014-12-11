jmd-scripts
===========

This repository contains scripts and documentation relevant to the workflow of the Joint Metadata Domain (task 5.4). If you would like to replicate the web portal, please refer to the installation instruction in the doc directory.

The JMD's workflow roughly comprises four stages, as illustrated below:

![workflow illustration](https://raw.githubusercontent.com/DASISH/jmd-scripts/master/workflow.png "JMD Workflow")

1. Fetching of original metadata records using the **OAI-PMH protocol**.
2. Performing **semantic mapping** into the JMD's internal
representation. In case metadata takes the form of CMDI, the definitions used are expanded and corresponding mapping tables will be generated. If not, the semantic mapper use static mapping tables.
3. Normalisation. This is the process of **conforming values to a standard representation**. For example, fields representing a date are checked and converted to a specific format.
4. Uploading. Once the records are normalised, they are uploaded to the **CKAN database**

Between stages, the metadata is stored on the file system to minimise
interdependency between the stages.

The main tasks are triggered by simple workflow scripts, found in this
repository, but the main body of work of the JMD is done in modules
that are stored in their own repositories


## Harvesting

OAI-PMH harvesting is a well defined process, so this part is
straightforward. We use our [OAI Harvest
Manager](https://github.com/TheLanguageArchive/oai-harvest-manager)
for it. See the [configuration file](harvester-config.xml) for
details. One thing of note is that formats to be harvested are mostly
defined based on the metadata schema (in which case, the harvester
performs a `ListMetadataFormats` query and harvests using all metadata
prefixes that fit the specified schema).


## Mapping

The mappings are stored and documented in a [separate
repository](https://github.com/DASISH/md-mapping).


## Web portal

The current implementation is based on [CKAN](http://ckan.org/), but
it could equally be built on top of other Solr based systems. Some
performance tweaks are used, which represented in the scripts.
