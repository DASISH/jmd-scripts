Lari Lampen (MPI-PL) / 2014
Currently these scripts assume that the working directory is
/home/work. We may parameterize assumptions like that at a later time.

Binyam (MPI-PL) / 2014

There are two types of workflow for uploading data into CKAN

1. uploading datasets one by one
2. bulk uploading (parallel uploading)

Most of the scripts in the workflow-scripts are for uploading datasets one by one. For bulk uploading, see below:

Bulk uploading
--------------

The ckanapi [1] supports bulk uploading. To do bulk uploading, we first need to create a jsonline file. This file  consists of json texts separated by '\n' [2]. We have a python script [3] that turns separate json files (datasets) into a single jsonline file. Once we have created a jsonline file or a set of jsonline files, then we can do bulk upload operations using ckanapi [1].

# For example

bulk operation (unzipped)
-------------------------
ckanapi load datasets -I g_cessda.jsonl -p 2 -r url -a apikey -l log_cessda

or

ckanapi load datasets -I g_cessda.jsonl -c /path/to/config -l log_cessda

Bulk upload (zipped)
----------------------
ckanapi load datasets -I g_cessda.jsonl.gz -z -p 2 -r url -a apikey -l log_cessda

or

ckanapi load datasets -I g_cessda.jsonl.gz -z -c /path/to/config -l log_cessda

[1] https://github.com/ckan/ckanapi

[2] http://jsonlines.org/

[3] https://github.com/DASISH/jmd-scripts/blob/master/workflow-scripts/make-jsonl.py
