import sys
import json
import requests
import untangle
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
import xml.etree.ElementTree as ET

import argparse


# We are using the 'requests' library as it makes simple username/password authentication easy (for this example, only)
# we also use the ElementTree library to simplify XML parsing/manipulation

# log in.
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def readConfig(cfg_file):
    if cfg_file == None:
        cfg_file = 'credentials.json'

    try:
       # using specified configfilename, grab url, un, & pwd from file
       with open(cfg_file) as data_file:
              data = json.load(data_file)
       return data

    except:
        # ex.msg is a string that looks like a dictionary
        print ("EXCEPTION: %s " % sys.exc_info())
        exit('couldnt open file %s' % cfg_file)

def queryViaRelevance(data, rVance):
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


# Function to filter out the names
def names(name):
    return name['value']

if __name__ == '__main__':
    config_filename = None
    myCfgData = readConfig(config_filename)

    username = myCfgData["credentials"]["username"]
    password = myCfgData["credentials"]["password"]
    baseurl = myCfgData["credentials"]['url']


    r = requests.get(baseurl+'/api/login',verify=False,auth=(username,password))
    if r.status_code != 200:
        print(r.status_code)

    r = requests.get(baseurl+'/api/fixlets/external/BES Support',verify=False,auth=(username,password))
    if r.status_code != 200:
        print(r.status_code)

    # point to the 'root' of the tree of XML data, then build a dictionary by filling two different arrays, then
    #       'zipping' (combining) together...
    root = ET.fromstring(r.text)

    i = []
    n = []

    print('starting search in results')
    for fixlet in root.findall('Fixlet'):
        n.append(fixlet.find('Name').text)
        i.append(fixlet.find('ID').text)

    print('creating dictionary')
    d = dict(zip(i, n))
    df0 = pd.DataFrame(dict(id=i, Name=n))

    # Now that we have the DataFrame, let's re-set the index to be the fixlet-id
    df1 = df0.set_index('id', inplace=None)

    print('\nAnd NOW... for something youll REALLY like (df1): ')
    print(df1)

    x = queryViaRelevance(myCfgData, "names of bes computers")
    y = [i.cdata for i in untangle.parse(x).BESAPI.Query.Result.Answer]
    z = pd.DataFrame(y)
    print("Here's y: ", y)
    print("Here's z: ", z.tail())
    print('Thats all')
