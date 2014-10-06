"""
Binyam Gebrekidan Gebre
@Max Planck Institute, 2014

HOW TO RUN
$ python md-postprocessor.py -i /path/to/input.json -o /path/to/output.json -c /path/to/config.txt
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

# initialize dictionaries for country and language mapping based on pycountry
MAP_DICTIONARIES = {}

LANGUAGES = {}
for ln in list(pycountry.languages):
    try:
        LANGUAGES[ln.alpha2] = ln.name
        LANGUAGES[ln.terminology] = ln.name
    except:
        pass
  
COUNTRIES = {}
for ct in list(pycountry.countries):
    try:
        COUNTRIES[ct.alpha2.lower()] = ct.name  
        COUNTRIES[ct.alpha3.lower()] = ct.name 
    except:
        pass 

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
	parser = argparse.ArgumentParser(description='Postprocesses a json file')
	parser.add_argument('-i','--srcFile',help='path to an input json file to be postprocessed')
	parser.add_argument('-c','--configFile',help='path to a configuration text file')
	parser.add_argument('-o','--dstFile', help='path to output json file')
	
	# parse command line arguments
	args = parser.parse_args()
	srcFile = args.srcFile
	configFile = args.configFile
	dstFile = args.dstFile
	
	if not (srcFile and configFile and dstFile):
	    print parser.print_help()
	    exit(1)
	
	# read input and config files
 	dataset = get_dataset(srcFile)
 	conf_data = get_conf(configFile)
 	
 	# postprocess the json file
 	new_dataset = postprocess(dataset,conf_data)
 	
 	# save output json to file
	save_data(new_dataset,dstFile)

if __name__ == "__main__":
	main()