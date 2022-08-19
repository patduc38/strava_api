import requests
import json
import sys 
#from pandas.json import json_normalize
import  pandas
import csv
import ga

try: 
    n=int(ga.readLastActivity())
except Exception as e:
    print("Can't get lastActivity",e)
    exit(1)

# Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
# Loop through all activities
url = "https://www.strava.com/api/v3/activities/"
access_token = strava_tokens['access_token']
# Get first page of activities from Strava with all fields
p=1
while 1 : 
    r = requests.get(url + '?access_token=' + access_token+"&per_page=200&page="+ str(p))
    p=p+1
    r = r.json()
    if not r : 
        break
    for s in  r :
        if s['id'] > n :
            print(str(p)+" " +str(s['id']))
            ga.gse(str(s['id']))
            ga.updateLastActivity(s['id'])

