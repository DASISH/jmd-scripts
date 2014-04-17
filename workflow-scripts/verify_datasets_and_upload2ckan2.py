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
import pickle
import copy
from time import time
import ckanapi

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
     
 
def main():
    dst_url = 'http://tlatest02.mpi.nl/ckan/'
    dst_apikey = '54870070-140f-4682-b914-63e82082233e'
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url')
    parser.add_argument('-a','--apikey')
    parser.add_argument('-c','--checksum')
    parser.add_argument('-s','--src')
    #parser.add_argument('-l','--log')

    args = parser.parse_args()
    checksum_pkl = args.checksum
    
    # loads a file containing filenames and their checksums
    if not checksum_pkl:
        print 'Error: checksum dictionary name missing'
        exit(1)

    checksum_table = get_checksum_table(checksum_pkl)
    
    if not args.src:
        print 'Error: source directory not given'
        exit(1)
        
    src_dir = args.src
    if src_dir.endswith('/'):
        src_dir = src_dir[:-1]

    groupNames=dict(map(lambda x:x.strip().split(),open('/home/work/work/group.txt').readlines()))
    _,group_name = os.path.split(os.path.split(src_dir)[0]) # extracts name of parent directory
    group_name = groupNames[group_name].lower()

    if group_name == 'cessda':
        exit(1)
	
    file_names = os.listdir(src_dir) # gets files in src, src is assumed to be a directory      
    f = open('april_upload_times.txt','a')
    f.write('#new session\n')
    ckan = ckanapi.RemoteCKAN(dst_url, dst_apikey)
    for i,fname in enumerate(file_names):
        if fname.endswith('.json'):
            path = os.path.join(args.src,fname)
            text = open(path).read()
            dataset = json.loads(text)
            dataset['groups'] = [{'name': group_name}]
            trim_MetadataSource(dataset)  # remove /home/work part to get /work/01-harvested/xxxx/and/so/on 
            checksum = get_checksum(dataset)
            if checksum_table.get(fname) != checksum: # if dataset is new or updated
                try:
                    t0 = time()
                    dataset['name'] = checksum
                    ckan.action.package_create(**dataset)
                    t = time() - t0 
                    f.write(str(t) + '\n')
                    checksum_table[fname] = checksum
                    print 'upload number =', i
                    print 'upload time =',t
                    print 'checksum of dataset =',checksum
                    print 'dataset =',dataset
                    #print text
                    print
                except ckanapi.ValidationError as e:
                    ckan.action.package_update(**dataset)
                    print i
                    print 'Error...'
                    print e
                    print dataset
                    print 
                except:
                    print i
                    print 'Error: skipping..'
                    print dataset 
                    #pickle.dump(checksum_table, open(checksum_pkl, "wb" ))
                    
    pickle.dump(checksum_table, open(checksum_pkl, "wb" ))
     
if __name__ == '__main__':
    main()
