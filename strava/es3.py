import requests
import json
#from pandas.json import json_normalize
import  pandas
import csv
import ga
# Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
# Loop through all activities
url = "https://www.strava.com/api/v3/activities/"
access_token = strava_tokens['access_token']
la=ga.readLastActivity()
print(la)

ga.updateLastActivity(int(la)+1)
la=ga.readLastActivity()
print(la)
    
