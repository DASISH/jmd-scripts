
input=/home/work/work/02-mapped # input directory with input of directories of json files
output=/home/work/work/03-harmonized # output directory where directories of json files are saved
config=config.txt #  normalization and replace rule file
checksumTable=/home/work/dict/ctable.pkl # dictionary of file names and their hashes

cd /home/work/jmd-scripts/workflow-scripts
sudo python md-harmonizer.py -i $input -o $output -c $config -d $checksumTable

