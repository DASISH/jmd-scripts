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
import csv
from urllib2 import urlopen
import logging
import copy
import hashlib
import cPickle as pickle


# Display progress logs on stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# regular expressions used in mapping dates of any format to utc format
UTC = re.compile(r'\d{4}(-\d{2}(-\d{2})?)?(T\d{2}:\d{2}(:\d{2}(\.\d{2})?)?[-+]\d{2}:\d{2})?')
YYYY = re.compile(r'(\d{4})')

# global variables for language and country mapping
u = urlopen('http://www-01.sil.org/iso639%2D3/iso-639-3.tab')
rows = list(csv.reader(u, delimiter='\t'))[1:]

LANGUAGES = {}
for row in rows:
    language_name = row[-2]
    if row[0]: LANGUAGES[row[0]] = language_name
    if row[1]: LANGUAGES[row[1]] = language_name
    if row[2]: LANGUAGES[row[2]] = language_name
    if row[3]: LANGUAGES[row[3]] = language_name
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
    changes date substring to UTC format
    returns matchingDate and remaining substring
    """
    # UTC format =  YYYY-MM-DDThh:mm:ss.ss[+_]hh:mm

    new_date = remaining = ''
    if UTC.search(old_date):
        new_date = UTC.search(old_date).group()
        remaining = old_date[old_date.find(new_date) + len(new_date):]
        new_date = new_date.replace("/","-")
    return new_date,remaining

def replace(dataset,facetName,old_value,new_value):
    """
    replaces old value with new value for a given facet
    """
    for facet in dataset:
        if str_equals(facet,facetName) and str_equals(dataset[facet],old_value):
            dataset[facet] = new_value
            return dataset
        if facet == 'extras':
            for extra in dataset[facet]:
                if extra['key'] == facetName and str_equals(extra['value'],old_value):
                    extra['value'] = new_value
                    return dataset
                elif extra['key'] == facetName and old_value == "*":
                    key = extra['value']
                    keys = key.split(";")
                    keys = map(lambda x:x.strip(),keys)
                    new_value = set()
                    for key in keys:
                        if ":" in key:
                            key = key.split(":")[-1].strip()
                        pValue = ''
                        try:
                            pValue = MAP_DICTIONARIES[facetName][key]
                        except KeyError:
                            pValue = key
                        for elem in pValue.split(';'):
                            new_value.add(elem)
                    extra['value'] = ";".join(new_value)
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
            if new_value not in dataset[facet]:
                dataset[facet] = dataset[facet].replace(old_value,new_value)
            else:
                dataset[facet] = dataset[facet].replace(old_value,new_value)
                temp = set(dataset[facet].split(";"))
                dataset[facet] = ";".join(temp)
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

def change_all_subdates(old_date):
    """
    changes all dates in old_dates to UTC formatted, comma separated dates
    input: dates (e.g. '1993-09-17/2000-02-12')
    output: UTC dates separated by commas (e.g. '1993-09-17;2000-02-12')
    """
    new_dates = []
    remaining = old_date
    while remaining:
        new_date, remaining = date2UTC(remaining)
        if new_date:
            new_dates.append(new_date)

    all_dates = ";".join(new_dates)
    return all_dates

def changeDateFormat(dataset,facetName,old_format,new_format):
    """
    changes date format from old format to a new format
    current assumption is that the old format is anything (indicated in the config file
    by * ) and the new format is UTC
    """
    for facet in dataset:
        if facet == 'extras':
            for extra in dataset[facet]:
                if str_equals(extra['key'],facetName) and old_format == '*':
                    if str_equals(new_format,'UTC'):
                        old_date = extra['value']
                        all_dates = change_all_subdates(old_date)
                        extra['value'] = all_dates
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

def get_groupName(path):
    """
    gets the group name from the path
    """
    return path.split('/')[5]

def add_OAI_Origin(dataset):
    """
    adds a facet for OAI origin
    """
    value = ""
    for extra in dataset['extras']:
        if extra['key'] == 'MetadataSource':
            value = extra['value'].split('/')[8] # splits path by / and takes the 8th entry as the provider name
            value = value.replace('_',' ')
            break
    dataset['extras'].append({"key":"OAI_Origin","value":value})

def trim_metadataSource(dataset):
    """
    updates a metadatasource field value; removes "/home/work"
    """
    for extra in dataset['extras']:
        if extra['key'] == 'MetadataSource':
            extra['value'] = extra['value'][10:]
            break

def get_checksum(json_data):
    """
    Calculates thecksum of the json_data, without including the MapperVersion
    """
    check_data = copy.deepcopy(json_data)
    index = 0
    for extra in check_data['extras']:
        if(extra['key'] == 'MapperVersion'):
            check_data['extras'].pop(index)
            break
        index+= 1
    checksum = hashlib.sha256(unicode(json.dumps(check_data))).hexdigest()
    return checksum

def get_checksum_table(checksum_pkl):
    """
    Loads checksum dictionary
    """
    if os.path.isfile(checksum_pkl):
        return pickle.load(open(checksum_pkl, 'rb'))
    else:
        return {}

def date2YYYYs(old_date):
    """
    extracts the YYYY (year) parts of the date
    input: comma separated dates
    output: comma separated years
    """

    dates = old_date.split(';')
    years = []
    for date in dates:
        yyyy = ''
        if UTC.search(date):
            yyyy = YYYY.search(date).group()
            if yyyy:
                years.append(yyyy)
    all_years = ";".join(years)
    return all_years

def createYearFacet(dataset,source_facet,new_facet):
    """
    creates a new facet called new_facet with value extracted from source_facet
    applies to CreationDate (CreationYear) and PublicationDate (PublicationYear)
    """
    yyyy = ''
    for extra in dataset['extras']:
        if str_equals(extra['key'],source_facet):
            old_date = extra['value']
            yyyys = date2YYYYs(old_date)
            dataset['extras'].append({"key":new_facet,"value":yyyys})
            return dataset
    return None

def createPublicationYearFacet(dataset):
    """
    creates/adds a new facet called PublicationYear from CreationDate
    """
    success = createYearFacet(dataset,"PublicationDate","PublicationYear")
    if success:
        return dataset
    else:
        createYearFacet(dataset,"CreationDate","PublicationYear")
        return dataset

def createCreationYearFacet(dataset):
    """
    creates/adds a new facet called CreationYear from CreationDate
    """
    createYearFacet(dataset,"CreationDate","CreationYear")
    return dataset


def get_user_input():
    """
    returns user input
    """
    parser = argparse.ArgumentParser(description='Harmonizes json files')
    parser.add_argument('-i','--input',help='input directory with json files')
    parser.add_argument('-c','--configFile',help='path to a configuration text file')
    parser.add_argument('-o','--output', help='output directory')
    parser.add_argument('-d','--dict', help='dictionary of files and their checksums')

    # parse command line arguments
    args = parser.parse_args()
    root = args.input
    configFile = args.configFile
    output = args.output
    checksum_pkl = args.dict

    if not (root and configFile and output and checksum_pkl):
        print parser.print_help()
        exit(1)

    return root, configFile, output, checksum_pkl

def main():

    # input from standard io
    srcDir, configFile, outputDir, checksum_pkl = get_user_input()

    checksum_table = get_checksum_table(checksum_pkl)
    # read config file from disk
    conf_data = get_conf(configFile)

    # walks through json files, harmonizes and saves files
    num = 0
    for parent, subdirs, fnames in os.walk(srcDir):
        srcFiles = filter(lambda x:x.endswith('.json'), fnames)
        if not srcFiles: continue

        # create output directories according to structure from input directories
        input = os.path.abspath(srcDir)
        absparent = os.path.abspath(parent)
        commonprefix = os.path.commonprefix([absparent,input])
        subdir = absparent.replace(commonprefix,"")
        outputpath = outputDir + subdir
        if not os.path.isdir(outputpath):
            os.makedirs(outputpath)

        # harmonize and save each json file
        for srcFile in srcFiles:
            path2file = os.path.join(absparent,srcFile)
            logging.info('harmonizing file [%d] %s', num, path2file)
            num += 1
            dataset = get_dataset(path2file)
            new_dataset = postprocess(dataset,conf_data)

            # add groupName
            group_name = get_groupName(path2file)
            dataset['groups'] = [{'name': group_name}]

            # add data provider
            add_OAI_Origin(dataset)

            # remove unnecessary part
            trim_metadataSource(dataset)

            # add hash ids (aka names) to datasets
            checksum = get_checksum(dataset)
            if checksum_table.get(srcFile) != checksum:
                dataset['name'] = checksum
                checksum_table[srcFile] = checksum

                # add title
                if "title" not in dataset:
                    dataset['title'] = 'Untitled'

                # add CreationYear facet
                createCreationYearFacet(dataset)

                # add PublicationYear facet
                createPublicationYearFacet(dataset)

                # save result as json
                fname = srcFile.replace('xml','json')
                path2file = os.path.join(outputpath,fname)
                save_data(new_dataset,path2file)
            else:
                logging.info('the above dataset exists')
        pickle.dump(checksum_table, open(checksum_pkl, "wb" ))



if __name__ == "__main__":
    main()

