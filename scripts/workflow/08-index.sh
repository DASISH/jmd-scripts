# this script is to be run when ckan uploading has been carried out with indexing disabled.

# changed to a directory where is ckan is installed
cd /usr/lib/ckan/default/src/ckan

# activate virtual environment 
. /usr/lib/ckan/default/bin/activate

# perform solr-indexing, for available options (see paster search-index --help)
paster search-index -o -i rebuild -c /etc/ckan/default/development.ini
