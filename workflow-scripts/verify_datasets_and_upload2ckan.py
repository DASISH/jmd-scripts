"""
Binyam Gebrekidan Gebre
@Max Planck Institute, 2013
"""


# 0) load dictionary of checksums
# 1) load directory with json files
# 2) calculate checksum
# 3) ifilter (fun,checkums)
# 4) imap(fun2,json_files)

import hashlib      
import simplejson as json
import itertools
import argparse
import os
import cPickle as pickle
import copy
from time import time

import sys
sys.path.append('/home/binyam/dasish_prototype/ckanapi')
import ckanapi


def add_DataProvider(dataset):
	"""
	adds data provider facet
	"""
	value = ""
	for extra in dataset['extras']:
		if extra['key'] == 'MetadataSource':
			value = extra['value'].split('/')[8] # splits path by / and takes the 8th entry as the provider name
			value = value.replace('_',' ')
			break
	dataset['extras'].append({"key":"DataProvider","value":value})

def trim_MetadataSource(dataset):
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
    """
    if os.path.isfile(checksum_pkl):
        return pickle.load(open(checksum_pkl, 'rb'))
    else:
        return {}
     
def split_structure(path):
    """
    splits a path to its parts (e.g. '/home/xxx/yy' to ['/','home','xxx','yy'])
    """
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url')
    parser.add_argument('-a','--apikey')
    parser.add_argument('-c','--checksum')
    parser.add_argument('-s','--src')
    #parser.add_argument('-l','--log')

    args = parser.parse_args()
    checksum_pkl = args.checksum
    
    dst_url = args.url
    dst_apikey = args.apikey

    # loads a file containing filenames and their checksums
    if not checksum_pkl:
        print 'Error: checksum dictionary name missing'
        exit(1)

    checksum_table = get_checksum_table(checksum_pkl)
    
    if not args.src:
        print 'Error: source file missing'
        exit(1)
    if not args.url:
       print 'Error: missing url'
       exit(1)
    if not args.apikey:
       print 'Error: missing apikey'
       exit(1)

    abs_path = args.src
    
    group_name = split_structure(abs_path)[5].lower() #  extracts group name
	
    f = open('august_upload_times.txt','a')
   # f.write('#new session\n')
    ckan = ckanapi.RemoteCKAN(dst_url, dst_apikey)
    
    if abs_path.endswith('.json'):
        text = open(abs_path).read()
        dataset = json.loads(text)
        dataset['groups'] = [{'name': group_name}]
        add_DataProvider(dataset) # adds the data provider facet and its value
        trim_MetadataSource(dataset)  # remove /home/work part to get /work/01-harvested/xxxx/and/so/on 
        checksum = get_checksum(dataset)
        _,fileName = os.path.split(abs_path)
        if checksum_table.get(fileName) != checksum: # if dataset is new or updated
            try:
                t0 = time()
                dataset['name'] = checksum
                ckan.action.package_create(**dataset)
                t = time() - t0 
                f.write(str(t) + '\n')
                checksum_table[fileName] = checksum
                print 'upload time =',t
                print 'checksum of dataset =',checksum
                print 'dataset =',dataset
                #print text
                print
            except ckanapi.ValidationError as e:
                ckan.action.package_update(**dataset)
                print 'Error...'
                print e
                print dataset
                print 
            except:
                print 'Error: skipping..'
                print dataset 
                #pickle.dump(checksum_table, open(checksum_pkl, "wb" ))
                    
    pickle.dump(checksum_table, open(checksum_pkl, "wb" ))
     
if __name__ == '__main__':
    main()
