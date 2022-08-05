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
id="3557000"
url = "https://www.strava.com/api/v3/segments/"+id
access_token = strava_tokens['access_token']
# Get first page of activities from Strava with all fields
r = requests.get(url + '?access_token=' + access_token)
#r = requests.get(url + '&segment_id=11184008')
r = r.json()
print(r)
try: 
    st="SELECT * from segments where id='"+id+"'"
    cur.execute(st)
    rows = cur.fetchall()
    print(rows)
    if len( rows) == 0:
        print("insert"+str(r['id']))
        st="""INSERT INTO segments (ID,name,activity_type,distance,average_grade,maximum_grade,elevation_high,elevation_low,total_elevation_gain,climb_category,city,state,country,private,starred) VALUES (? ,?, ?, ?, ?, ?, ?, ?, ?, ?,? ,?, ?, ?, ?)"""
        try:
            cur.execute(st,(r['id'],r['name'],r['activity_type'],r['distance'],r['average_grade'],r['maximum_grade'],r['elevation_high'],r['elevation_low'],r['total_elevation_gain'],r['climb_category'],r['city'],r['state'],r['country'],r['private'],r['starred']))
        except sqlite3.IntegrityError:
            print("segment already added")
    else: 
        print("already segments")
except KeyError as e :
    print("key error encountered"+e)
con.commit()

#for row in cur.execute('select * from segment_efforts'):
#    print(row)
con.close()
