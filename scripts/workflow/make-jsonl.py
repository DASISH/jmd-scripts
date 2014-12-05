"""
Binyam Gebrekidan Gebre
@Max Planck Institute, 2014

HOW TO RUN
$ python md-harmonizer.py -i /path/to/json -o /path/to/output.jsonline
Input: a directory that has json files
Output:jsonline file 
"""

import os
import argparse
import re
import simplejson as json
import io
import codecs
import pycountry 
import csv
from urllib2 import urlopen
import logging


# Display progress logs on stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

   
def get_dataset(srcFile):
    """
    reads file from disk and returns json text
    """
    text = open(srcFile).read()
    dataset = json.loads(text)
    return dataset


def get_user_input():
    """
    returns user input
    """
    parser = argparse.ArgumentParser(description='Makes jsonline file')
    parser.add_argument('-i','--input',help='input directory with json files')
    parser.add_argument('-o','--output', help='output file name')

    # parse command line arguments
    args = parser.parse_args()
    root = args.input
    output = args.output

    if not (root and output):
        print parser.print_help()
        exit(1)
    
    return root, output
    			
def main():
    
    # input from standard io
    srcDir, outputFile = get_user_input()
    
    
    # walks through json files and saves them as json lines
    batchSize = 100
    f = io.open(outputFile,'w',encoding='utf-8')
    jsonlines = ''
    num = 0
    for parent, subdirs, fnames in os.walk(srcDir):
        srcFiles = filter(lambda x:x.endswith('.json'), fnames) 
        if not srcFiles: continue
        
        absparent = os.path.abspath(parent)
        for srcFile in srcFiles:
            path2file = os.path.join(absparent,srcFile)
            logging.info('[%d] reading file ... %s',num, path2file)
            dataset = get_dataset(path2file)
            jsontext = unicode(json.dumps(dataset,ensure_ascii=False))
            jsonlines = jsonlines + jsontext + '\n'
            num += 1
            if num%batchSize == 0:
                f.write(jsonlines)
                jsonlines = ''
    
    if jsonlines:
        f.write(jsonlines.strip())

if __name__ == "__main__":
	main()
