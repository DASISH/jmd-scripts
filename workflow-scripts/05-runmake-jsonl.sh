
# Make jsonlines
input=/home/work/work/03-harmonized # input directory where all harmonized/normalized json files are available
output=/home/work/data2upload.jsonl # output file where all json files are put togther into one big json line file

cd /home/work/jmd-scripts/workflow-scripts
sudo python make-jsonl.py -i $input -o $output
