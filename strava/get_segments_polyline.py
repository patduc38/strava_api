import requests
import json
import sqlite3

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

# url = "https://www.strava.com/api/v3/activities/"+id

access_token = strava_tokens['access_token']
#r = requests.get(url + '?access_token=' + access_token)
#r = r.json()

cur = con.cursor() 
st="SELECT ID from segments;"
cur.execute(st)
rows = cur.fetchall()
for row in rows:
    if int(row[0]) <= 38247298: 
          continue
    url = "https://www.strava.com/api/v3/segments/"+str(row[0])
    r = requests.get(url + '?access_token=' + access_token)
    if r.status_code == 404:
          continue
    print("Pat add r=", row[0],r)
    r = r.json()
    polyline=r['map']['polyline']
    print("Pat Add", polyline,str(row[0]) )
    print("Adding in segment_info:")
    if polyline != "":
        st="""INSERT INTO segment_info (segment_ID,polyline) VALUES (? ,?)"""
        try:
            cur.execute(st,(str(row[0]),polyline))
            con.commit()            
        except Exception as e :
                    print("Error encountered while adding segment e=",e)

#for row in cur.execute('select * from segment_efforts'):
#    print(row)
con.close()
