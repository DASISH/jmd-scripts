"""
Binyam Gebrekidan Gebre
@Max Planck Institute, 2014

HOW TO RUN
$ python md-harmonizer.py -i /path/to/input.json -o /path/to/output.json -c /path/to/config.txt
Input: json file (the input comes from the output of the mapper)
Configuration file (this is a text file, where actions or rules are specified, In the scripts folder, you can see the format of the config.tx)
Output:json file (the output of the postprocessor is another json file ready to be validated and/or uploaded to CKAN) 
"""

import numpy as np
import os
import argparse
import re
import simplejson as json
import io
import codecs
import pycountry 
<<<<<<< HEAD
import csv
from urllib2 import urlopen
=======
# pycountry provides the ISO databases for the standards:
# 639 for languages
# 3166 for countries
>>>>>>> 4fdb5cef7134f1d7b56ad1e8b189c393066c5a54

u = urlopen('http://www-01.sil.org/iso639%2D3/iso-639-3.tab')
rows = list(csv.reader(u, delimiter='\t'))[1:]

LANGUAGES = {}
for row in rows:
    LANGUAGES[row[0]] = row[-2] # key: the first field, value: the second from last field
for ln in list(pycountry.languages):
    try:
        LANGUAGES[ln.alpha2] = ln.name
        #LANGUAGES[ln.terminology] = ln.name
    except:
        pass
        
  
COUNTRIES = {}

for ct in list(pycountry.countries):
    try:
        COUNTRIES[ct.alpha2.lower()] = ct.name  
        COUNTRIES[ct.alpha3.lower()] = ct.name 
    except:
        pass
    

MAP_DICTIONARIES = {}

MAP_DICTIONARIES["Language"] = LANGUAGES
MAP_DICTIONARIES["Country"] = COUNTRIES

   
def get_dataset(srcFile):
    """
    reads file from disk and returns json text
    """
    text = open(srcFile).read()
    dataset = json.loads(text)
    return dataset
    
def get_conf(configFile):
    """
    reads config file 
    """
    f = codecs.open(configFile, "r", "utf-8")
    rules = f.readlines()
    rules = filter(lambda x:len(x.strip()) != 0,rules) # removes empty lines
    return rules
    
def save_data(dataset,dstFile):
    """
    saves a json file
    """
    with io.open(dstFile, 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(dataset, indent = 4,ensure_ascii=False)))

def str_equals(str1,str2):
    """
    performs case insensitive string comparison by first stripping trailing spaces 
    """
    return str1.strip().lower() == str2.strip().lower()
    
    
def date2UTC(old_date):
    """
    changes date to UTC format
    """
    # UTC format =  YYYY-MM-DDThh:mm:ssZ
    utc = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
   
    utc_year = re.compile(r'\d{4}') # year (4-digit number)
    if utc.search(old_date):
        new_date = utc.search(old_date).group()
        return new_date
    elif utc_year.search(old_date):
        year = utc_year.search(old_date).group()
        new_date = year + '-07-01T11:59:59Z'
        return new_date
    else:
        return '' # if converting cannot be done, make date empty
    
       
def replace(dataset,facetName,old_value,new_value):
    """
    replaces old value with new value for a given facet
    """
    for facet in dataset:
        if str_equals(facet,facetName) and dataset[facet] == old_value:
            dataset[facet] = new_value
            return dataset
        if facet == 'extras':
            for extra in dataset[facet]:
                if extra['key'] == facetName and extra['value'] == old_value:
                    extra['value'] = new_value
                    return dataset
                elif extra['key'] == facetName and old_value == "*":
                    key = extra['value']
                    try:
                        new_value = MAP_DICTIONARIES[facetName][key]
                        extra['value'] = new_value
                    except:
                        pass
                    return dataset
                else:
                    pass
                
    return dataset

def replace_token(dataset,facetName,old_value,new_value):
    """
    replaces old value with new value for a given facet
    """
    for facet in dataset:
        if str_equals(facet,facetName) and old_value in dataset[facet]:
            dataset[facet] = dataset[facet].replace(old_value,new_value)
            return dataset
        if facet == 'extras':
            for extra in dataset[facet]:
                if extra['key'] == facetName and old_value in extra['value']:
                    extra['value'] = extra['value'].replace(old_value,new_value)
                    return dataset
                else:
                    pass
                
    return dataset
    
def truncate(dataset,facetName,old_value,size):
    """
    truncates old value with new value for a given facet
    """
    for facet in dataset:
        if facet == facetName and dataset[facet] == old_value:
            dataset[facet] = old_value[:size]
            return dataset
        if facet == 'extras':
            for extra in dataset[facet]:
                if extra['key'] == facetName and extra['value'] == old_value:
                    extra['value'] = old_value[:size]
                    return dataset
    return dataset

def changeDateFormat(dataset,facetName,old_format,new_format):
    """
    changes date format from old format to a new format
    current assumption is that the old format is anything (indicated in the config file 
    by * ) and the new format is UTC
    """
    for facet in dataset:
        if str_equals(facet,facetName) and old_format == '*':
            if str_equals(new_format,'UTC'):
                old_date = dataset[facet]
                new_date = date2UTC(old_date)
                dataset[facet] = new_date
                return dataset
        if facet == 'extras':
            for extra in dataset[facet]:
                if str_equals(extra['key'],facetName) and old_format == '*':
                    if str_equals(new_format,'UTC'):
                        old_date = extra['value']
                        new_date = date2UTC(old_date)
                        extra['value'] = new_date
                        return dataset
    return dataset
    
         

def postprocess(dataset,rules):
    """
    changes dataset field values according to configuration
    """   
    for rule in rules:
        # rules can be checked for correctness
        if rule.startswith('#'): continue
  
        assert(rule.count(',,') == 5),"a double comma should be used to separate items"
        
        rule = rule.split(',,') # splits the each line of config file 
        groupName = rule[0]
        datasetName = rule[1]
        facetName = rule[2]
        old_value = rule[3]
        new_value = rule[4]
        action = rule[5]
                    
        r = dataset.get("group",None)
        if groupName != '*' and  groupName != r: continue

        r = dataset.get("DataProvider",None)
        if datasetName != '*' and datasetName != r: continue
        
        #print action
        if str_equals(action,"replace"):
            # old_value refers to old text, which we want to replace by new text 
            dataset = replace(dataset,facetName,old_value,new_value)
        elif str_equals(action,"replace_token"):
            # old_value refers to old text, which we want to replace by new text 
            dataset = replace_token(dataset,facetName,old_value,new_value)
        elif str_equals(action,"truncate"):
            # old_value refers to text given or any (represented by '*')
            # new_value refers to the number of characters to truncate the text to
            dataset = replace(dataset,facetName,old_value,new_value)
        elif str_equals(action,"changeDateFormat"):
            # old_value refers to any date format (represented by '*')
            # new_value refers to UTC format
            dataset = changeDateFormat(dataset,facetName,old_value,new_value)
        elif action == "another_action":
            pass
        else:
            pass
    
    return dataset
    
def main():
    parser = argparse.ArgumentParser(description='Harmonizes json files')
    parser.add_argument('-i','--input',help='input directory with json files or just json file')
    parser.add_argument('-c','--configFile',help='path to a configuration text file')
    parser.add_argument('-o','--output', help='output directory or output file')

    # parse command line arguments
    args = parser.parse_args()
    input = args.input
    configFile = args.configFile
    output = args.output


    if not (input and configFile and output):
        print parser.print_help()
        exit(1)

    # read config file
    conf_data = get_conf(configFile)


    # checks if input is directory, otherwise assumes a single xml file
    srcFiles = None
    if os.path.isdir(input):
        srcFiles = filter(lambda x:x.endswith('.json'), os.listdir(input))
    else: 
        srcFiles = [input]
    
    # checks if output (sub)directory exists, otherwise makes dirs recursively
    if not os.path.isdir(output):
        os.makedirs(output)
        
    for srcFile in srcFiles:
        dataset = get_dataset(srcFile)
        new_dataset = postprocess(dataset,conf_data)
        
        _,fname = os.path.split(srcFile)
        fname = fname.replace('xml','json')
        output = os.path.join(os.path.abspath(output),fname)
        
        save_data(new_dataset,output)	    

if __name__ == "__main__":
	main()
