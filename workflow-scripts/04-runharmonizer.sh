<<<<<<< HEAD
input=/home/work/work/02-mapped-old # input directory with input of directories of json files
output=/home/work/work/03-harmonized-test # output directory where directories of json files are saved
config=config.txt #  normalization and replace rule file
checksumTable=ctable.pkl # dictionary of file names and their hashes

cd /home/work/jmd-scripts/workflow-scripts
sudo python md-harmonizer.py -i $input -o $output -c $config -d $checksumTable

=======
python md-harmonizer.py -i /home/work/work/02-mapped -c /home/work/jmd-scripts/workflow-scripts/config.txt -o /home/work/work/03-harmonized
>>>>>>> 387c294bc69137235bac545b680f160d1c3e2747
