import requests
import json
#from pandas.json import json_normalize
import  pandas
import sys
import sqlite3

if (len(sys.argv)<2):
        n=18862079
else :
        n=sys.argv[1]
con = sqlite3.connect('strava.db')
cur = con.cursor()

with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)


st="SELECT * from segments order by ID"
cur.execute(st)
rows = cur.fetchall()
for row in rows :         
    print(row[0],row[1])
    if (int(row[0])< int(n)) : 
        print("skip ",row[0])
        continue
    url = "https://www.strava.com/api/v3/segments/"+str(row[0])
#url = "https://www.strava.com/api/v3/activities/"
#url = "https://www.strava.com/api/v3/segment_efforts/"
    access_token = strava_tokens['access_token']
# Get first page of activities from Strava with all fields 
    r = requests.get(url + '?access_token=' + access_token)
    r = r.json()
    try :
        isStarred=r['starred']
    except Exception as e :
        print("could not handle",str(row[0]),e,r)
        continue   
    if not isStarred == row[14] :
        print("c'est different dans strava et dans sqlite ", row[14])
        st="UPDATE segments  SET starred = " +  str(int(isStarred== True)) + " WHERE ID='"+str(row[0])+"';"
        cur.execute(st)
        con.commit()
 

#for row in cur.execute('select * from segment_efforts'):
#    print(row)
con.close()


exit(1)
# Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
# Loop through all activities
url = "https://www.strava.com/api/v3/segments/5855232"
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
