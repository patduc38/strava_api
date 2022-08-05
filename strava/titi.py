import requests
import json
#from pandas.json import json_normalize
import  pandas
import csv
# Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
# Loop through all activities
url = "https://www.strava.com/api/v3/activities/7509204661"
#url = "https://www.strava.com/api/v3/activities/"
#url = "https://www.strava.com/api/v3/segment_efforts/"
access_token = strava_tokens['access_token']
# Get first page of activities from Strava with all fields
r = requests.get(url + '?access_token=' + access_token)
#r = requests.get(url + '&segment_id=11184008')
r = r.json()
df = pandas.json_normalize(r)
#print(df)    
print(json.dumps(r))    
