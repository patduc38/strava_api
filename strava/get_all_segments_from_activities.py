import requests
import json
#from pandas.json import json_normalize
import  pandas
import csv
import ga

# Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
access_token = strava_tokens['access_token']

 
with open('activities') as f:
    while True:
        line = f.readline()
        if not line:
            break
        
        print("Treating activity ", line)
        url = "https://www.strava.com/api/v3/activities/"+line
        r = requests.get(url + '?access_token=' + access_token)
        r = r.json()

        try:
            for s in r['segment_efforts']:
                sid=str(s['segment']['id'])
                ga.addsegment(sid)
        except Exception as e:
            print(f"key error encountered when treating activity or e={e!r}",line)
            exit(1)
