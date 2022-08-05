import requests
import json
#from pandas.json import json_normalize
import  pandas
import csv
# Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
# Loop through all activities
with open('activities') as f:
    while True:
        line = f.readline()
        if not line: 
            break
        url = "https://www.strava.com/api/v3/activities/"+line
        access_token = strava_tokens['access_token']
        r = requests.get(url + '?access_token=' + access_token)
        r = r.json()
        print(json.dumps(r))    
