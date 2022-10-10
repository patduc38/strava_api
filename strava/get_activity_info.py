import requests
import json
import sys
import  pandas
import csv
import sqlite3

#connection to sqlite db strava.db
con = sqlite3.connect('strava.db')    
cur = con.cursor()

# Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
# Loop through all activities
#url = "https://www.strava.com/api/v3/activities/7509204661"
url = "https://www.strava.com/api/v3/activities/"+sys.argv[1]
#url = "https://www.strava.com/api/v3/activities/"
#url = "https://www.strava.com/api/v3/segment_efforts/"
access_token = strava_tokens['access_token']
# Get first page of activities from Strava with all fields
r = requests.get(url + '?access_token=' + access_token)
#r = requests.get(url + '&segment_id=11184008')
r = r.json()

print ("Pat Add", r)
print ("Pat Add", r['gear']['name'])

for s in r['segment_efforts']:
    print ("Pat Add", s)

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
    elapsed_timep=str(s['elapsed_time'])
    print("elapsed_time="+str(s['elapsed_time']))
    average_watts=str(s['average_watts'])
    print("average_watts="+str(s['average_watts']))
    average_grade=str(s['segment']['average_grade'])
    print("average_grade="+str(s['segment']['average_grade']))
    elevation=str(round(s['segment']['elevation_high']-s['segment']['elevation_low']))
    print("elevation="+str(round(s['segment']['elevation_high']-s['segment']['elevation_low'])))
    start_date_local=str(s['start_date_local'])
    print("start_date_local="+str(s['start_date_local']))
    st="INSERT INTO segment_efforts (ID,segment_ID,segment_name,segment_distance,athlete_ID,moving_time,average_watts,average_rate,elevation,start_date_local) VALUES (" + seid + "," + sid + ", + \"%s\" + ," + distance + "," + athlete_id + "," + moving_time + "," + average_watts + "," + average_grade + "," + elevation + "," + start_date_local+")"
    print("st="+st)
   # st="""INSERT INTO segment_efforts (ID,segment_ID,segment_name,segment_distance,athlete_ID,moving_time,average_watts,average_rate,elevation,start_date_local) VALUES (? ,?, ?, ?, ?, ?, ?, ?, ?, ?)"""
   # try: 
   #     cur.execute(st,(seid,sid,name,distance,athlete_id,moving_time,average_watts,average_grade,elevation,start_date_local))
   # except sqlite3.IntegrityError:
   #q     print("segment effort already added")

con.commit()

con.close()
