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
      con = sqlite3.connect('strava.db')
      cur = con.cursor()

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

              if elevation != "":
                  st="INSERT INTO segment_efforts (ID,segment_ID,segment_name,segment_distance,athlete_ID,moving_time,average_watts,average_rate,elevation,start_date_local) VALUES (" + seid + "," + sid + ", + \"%s\" + ," + distance + "," + athlete_id + "," + moving_time + "," + average_watts + "," + average_grade + "," + elevation + "," + start_date_local+")"
                  st="""INSERT INTO segment_efforts (ID,segment_ID,segment_name,segment_distance,athlete_ID,moving_time,average_watts,average_rate,elevation,start_date_local) VALUES (? ,?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                  try:
                      cur.execute(st,(seid,sid,name,distance,athlete_id,moving_time,average_watts,average_grade,elevation,start_date_local))
                  except sqlite3.IntegrityError as e:
                      print("segment effort already added or ee=",e)
                  # check if seglment exist insegments table and if not add it

      except KeyError as e:
          print("key error encountered or ee=",e)
      con.commit()

      #for row in cur.execute('select * from segment_efforts'):
      #    print(row)
      con.close()
