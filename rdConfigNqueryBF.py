import sys

import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
import xml.etree.ElementTree as ET
import xmltodict

import argparse


# We are using the 'requests' library as it makes simple username/password authentication easy 
# and reproducable. We also demonstrate the use of ElementTree & XmlToDict for parsing/manipulation
# of the resultant XML payload extracted from BF

def readConfig(cfg_file):
    if cfg_file == None:
        cfg_file = '../BFcredentials.json'

    try:
       # using specified configfilename, grab url, un, & pwd from file
       with open(cfg_file) as data_file:
           return json.load(data_file)

    except:
        # ex.msg is a string that looks like a dictionary
        print ("EXCEPTION: %s " % sys.exc_info())
        exit('couldnt open file %s' % cfg_file)

def queryBFviaRelevance(data, rVance):
       url = data["credentials"]["url"]
       username = data["credentials"]["username"]
       password = data["credentials"]["password"]

       if password == '':
           password = input("Enter password in quotes, please: ")

       resp = requests.get(url+'/api/login', verify=False, auth=(username, password))
       if resp.status_code != 200:
           data = str(resp.text)
           sys.exit(-1)

       myRequest=url + '/api/query?relevance=' + rVance
       resp = requests.get(myRequest, verify=False, auth=(username, password))
       if resp.status_code != 200:
           print( "Uh, oh! Status was {0}".format(resp.status_code ))
       return resp.text


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    pd.options.display.max_colwidth = 100
    config_filename = None
    myCfgData = readConfig(config_filename)

    username = myCfgData["credentials"]["username"]
    password = myCfgData["credentials"]["password"]
    baseurl = myCfgData["credentials"]['url']

# Attempt to first login to BF to verify 'connetivity'
    r = requests.get(baseurl+'/api/login',verify=False,auth=(username,password))
    if r.status_code != 200:
        print(r.status_code)
        sys.exit(-1)

# Attempt to get the names and ids of all the 'BES Support' fixlets
    r = requests.get(baseurl+'/api/fixlets/external/BES Support',verify=False,auth=(username,password))
    if r.status_code != 200:
        print(r.status_code)
        sys.exit(-1)
    #else:
    #    print(r.text)

    # Using ElementTree, point 'root' to the base of the returned information & extract
    #    The ids and names from the XML by looping through the resultant list
    root = ET.fromstring(r.text)    
    i = []
    n = []
    for fixlet in root.findall('Fixlet'):
        n.append(fixlet.find('Name').text)
        i.append(fixlet.find('ID').text)

# With the two arrays 'zipped' into a dictionary create a pandas dataframe & print first 10 rows
    df0 = pd.DataFrame.from_dict(dict(zip(i,n)), orient='index')
    print(df0.head())

    # So, now let's use our 'helper-function' queryBFviaRelevance(), and parse the result
    # using xmltodict() instead of above-used i,n loop
    xml = queryBFviaRelevance(myCfgData, 'names of bes computers')
    
    # [note that if I use the relevance to 'intersperse' the results with, say, '>' characters
    #    it will facilitate parsing the results in order to print].
    
    # Incidentally, xmltodict.parse(xml) returns an ordered-dictionary of dictionaries, so we
    #    then have to narrow the reference to the highest-level dictionary to the individual
    #    elements we want to extract ...['BESAPI']['Query']['Result']['Answer'], loop through 
    #    THAT dictionary, and extract the elements titled '#text', so we can print them.

    # When we later use this sample in a real-world scenario, we'll employ lambda functions 
    #        to parse the returned XML &, say, extract computer-names (note that they have 
    #        1 parameter & return a dataframe), e.g. something like 
    #        ResponseDataframe = 
    #            pd.DataFrame([i.cdata for i in untangle.parse(x).BESAPI.Query.Result.Answer])
    # replaced with:
    #           computersLf2 = lambda x: pd.DataFrame([i.cdata.split(">") for i in untangle.parse(x).BESAPI.Query.Result.Answer])
    #
    # THAT way, we 'encapsulate' the 'knowledge' of what the dictionary 'looks like' in one spot,
    #    the particular 'lambda' function
    print("\nAnd here we've got the names of all ({0}) computers:\n".format(df0.size))
    print([i['#text'] for i in xmltodict.parse(xml)['BESAPI']['Query']['Result']['Answer']])
    
    print('\nDone...')
