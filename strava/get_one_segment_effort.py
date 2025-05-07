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



#connection to sqlite db strava.db
try:
      # Get the tokens from file to connect to Strava
      with open('strava_tokens.json') as json_file:
              strava_tokens = json.load(json_file)

      url = "https://www.strava.com/api/v3/activities/12291685922"
      #url = "https://www.strava.com/api/v3/activities"

      access_token = strava_tokens['access_token']
      r = requests.get(url + '?access_token=' + access_token)
      print("Pat Add delete act=",r,r.status_code) 
      r = r.json()
except Errors as e:
        print("there is an error")
