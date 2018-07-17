import sys
import json
import requests
import untangle
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
#import xml.etree.ElementTree as ET

import argparse


# We are using the 'requests' library as it makes simple username/password authentication easy (for this example, only)
# we also use the ElementTree library to simplify XML parsing/manipulation

# log in.

def readConfig(cfg_file):
    if cfg_file == None:
        cfg_file = '../credentials.json'

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


# Sample lambda function to parse returned XML & extract computer-names (note it has 1 parameter & 
#        returns a dataframe
#        previously: ResponseDataframe = pd.DataFrame([i.cdata for i in untangle.parse(x).BESAPI.Query.Result.Answer])
computersLf1 = lambda x: pd.DataFrame([i.cdata for i in untangle.parse(x).BESAPI.Query.Result.Answer])
computersLf2 = lambda x: pd.DataFrame([i.cdata.split(">") for i in untangle.parse(x).BESAPI.Query.Result.Answer])

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    pd.options.display.max_colwidth = 100
    config_filename = None
    myCfgData = readConfig(config_filename)

    username = myCfgData["credentials"]["username"]
    password = myCfgData["credentials"]["password"]
    baseurl = myCfgData["credentials"]['url']


    r = requests.get(baseurl+'/api/login',verify=False,auth=(username,password))
    if r.status_code != 200:
        print(r.status_code)

#    r = requests.get(baseurl+'/api/fixlets/external/BES Support',verify=False,auth=(username,password))
#    if r.status_code != 200:
#        print(r.status_code)

