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

try :
      id=12291685922

      # Get the tokens from file to connect to Strava
      with open('strava_tokens.json') as json_file:
              strava_tokens = json.load(json_file)

      url = "https://www.strava.com/api/v3/activities/"+id

      access_token = strava_tokens['access_token']
      r = requests.get(url + '?access_token=' + access_token)
      r = r.json()

      try:
          for s in r['segment_efforts']:
              seid=str(s['id'])
              print("ID="+str(id))
              sid=str(s['segment']['id'])
              print("segmentID="+str(s['segment']['id']))
              name=s['name']
              print("name="+s['name'])
              distance=str(s['segment']['distance'])
              print("distance="+str(s['segment']['distance']))
              athlete_id=str(s['athlete']['id'])
              print("athleteID="+str(s['athlete']['id']))
              moving_time=str(s['moving_time'])
              print("moving_time="+str(s['moving_time']))
              try :
                  average_watts=str(s['average_watts'])
              except KeyError:
                  average_watts="0"
              print("average_watts="+average_watts)
              average_grade=str(s['segment']['average_grade'])
              print("average_grade="+str(s['segment']['average_grade']))
              try :
                  elevation=str(round(s['segment']['elevation_high']-s['segment']['elevation_low']))
              except TypeError:
                  elevation=""
              print("elevation="+elevation)
              start_date_local=str(s['start_date_local'])
              print("start_date_local="+str(s['start_date_local']))


