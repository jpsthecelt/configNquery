import requests
import sys
import json
import argparse

    # parse commandline and get appropriate passwords/configuration-items
    #
#    parser = argparse.ArgumentParser(description='Get configuration-filename and item to dump')
#    parser.add_argument('-f', action='store', dest='config_filename',
#                        help='Config filename ')
#    parser.add_argument('-c', action='store', dest='change_item',
#                        help='Plutora Changefile (in JSON)")')
#    results = parser.parse_args()
#    change_entity = results.change_item
#
#    config_filename = results.config_filename
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
       else:
           print(resp.status_code)

       myRequest=url + '/api/query?relevance=' + rVance
       resp = requests.get(myRequest, verify=False, auth=(username, password))
       if resp.status_code != 200:
           print( "Uh, oh! Status was {0}".format(resp.status_code ))
       print(resp.text)


if __name__ == '__main__':
    config_filename = None
    myData = readConfig(config_filename)
    print(myData)
    print(queryViaRelevance(myData, 'names of bes computers'))



