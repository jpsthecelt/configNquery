import sys
import json
import argparse
import requests
import urllib3
import untangle
import xmltodict
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
#import xml.etree.ElementTree as ET

# AUTHOR:   JSinger
# INCEPT:   2.15.2019
# NAME:     rdBFfixletInfo.py
# DESCRIPTION:
#           Extract information about fixlets from their respective sites.
#
# ASSUMPTIONS:
#           Using BF ReST API and 'relevance' language to query; this assumes you first login, and that you
#           have access to the server at port 52311, as well as being familiar with the hows and whys
#           of the BigFix-IBM-HCL relevance-language 

# IMPLEMENTATION DETAILS:
#           Note that our 'relevance' uses the 'sandwich'-technique to pack a bunch of '>'-separated text into 
#           one query; we later use a specifi lambda-function to extract (split) these elements into something
#           we can turn into a dictionary, and thence a pandas dataframe.


# In this code, We demonstrate using different libraries: requests, emementtree, xmltodict, and untangle.
#
# We are using the 'requests' library to make simple username/password authentication easy (for this example, only)
# we also use the ElementTree, xmltodict, and untanble libraries to simplify XML parsing/manipulation

# get/execute log in.
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

# Using the supplied credential/url (data), use the relevance to query the BF database & 
#       return information 
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

       if rVance == '':
           rVance = input("Enter your relevance in quotes, please: ")

       myRequest=url + '/api/query?relevance=' + rVance
       resp = requests.get(myRequest, verify=False, auth=(username, password))
       if resp.status_code != 200:
           print( "Uh, oh! Status was {0}".format(resp.status_code ))
       return resp.text


# Sample lambda functions to parse returned XML & extract computer-names (note it has 1 parameter & 
#        returns a dataframe
#        previously: ResponseDataframe = pd.DataFrame([i.cdata for i in untangle.parse(x).BESAPI.Query.Result.Answer])
# fixletsLf = lambda x: pd.DataFrame([i.cdata.split(">") for i in xmltodict.parse(x)['BESAPI']['Query']['Result']['Answer']])
fixletsLf1 = lambda x: pd.DataFrame([i['#text'].split('>') for i in xmltodict.parse(x)['BESAPI']['Query']['Result']['Answer']])

computersLf1 = lambda x: pd.DataFrame([i.cdata for i in untangle.parse(x).BESAPI.Query.Result.Answer])
computersLf2 = lambda x: pd.DataFrame([i.cdata.split(">") for i in untangle.parse(x).BESAPI.Query.Result.Answer])

# Main routine which handles initialization, reading login-info/url from config-file, and 
#      orchestrates quering BF using relevance, parsing, and outputting data to the indicated file.
#
if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    pd.options.display.max_colwidth = 100
    config_filename = None
    myCfgData = readConfig(config_filename)

    username = myCfgData["credentials"]["username"]
    password = myCfgData["credentials"]["password"]
    baseurl = myCfgData["credentials"]['url']


    r = requests.get(baseurl+'/api/login',verify=False,auth=(username,password))
    if r.status_code != 200:
        print(r.status_code)

# Example of sample explicit-query without using the queryBFviaRelecance() routine:
#
#    r = requests.get(baseurl+'/api/fixlets/external/BES Support',verify=False,auth=(username,password))
#    if r.status_code != 200:
#        print(r.status_code)
#    else:
#        print(r.text)

# After accepting relevance and filename from user, use improved-method to query BF data, format, and
#       output to file.

    r = ''
    relevance =  '(id of it as string%26 %22%3e%22 %26 name of it%26 %22%3e%22 %26 name of site of it%26 %22%3e%22 %26 relevance of it%26 %22%3e%22 %26 (script of default action of it | "<no script>")) of fixlets of bes site whose (name of it as lowercase contains "enterprise security")'

    print('\n...We need something like {0}\n'.format(relevance))
    # Now, go get all the fixlets and turn the result into a dictionary
    if len(r) == 0:
       r = input("Enter desired relevance in quotes, please: ")
    r = relevance

    fn = ''
    if len(fn) == 0:
       fn = input("\nEnter desired output-filename.csv (without quotes), please: ")
    else:
       fn = 'saved_query.csv'

# Call query-routine, supplying returned XML.
    d0 = fixletsLf1(queryBFviaRelevance(myCfgData, relevance))
    d0.to_csv(fn, sep=',', encoding='utf-8')

    print('\nJust output {0} fixlets to file {1}'.format(len(d0), fn))
