import requests
import json
import sys
import  pandas
import csv
import sqlite3


# true if activity has been treated 
def isActivityPresent(a):
    #connection to sqlite db strava.db
    con = sqlite3.connect('strava.db')
    cur = con.cursor()

    try:
        st="SELECT * FROM segment_efforts WHERE activity_ID =  '"+str(a)+"' ;"
        cur.execute(st)
        rows = cur.fetchall()
        con.close()
        if len(rows) > 0:
            return True
    except KeyError as e :
        print("key error encountered or e=",e)
        con.close()
    return False

# get Last activity
def readLastActivity():
    #connection to sqlite db strava.db
    con = sqlite3.connect('strava.db')
    cur = con.cursor()
    la=0

    try:
        st="SELECT value  FROM settings WHERE key =  'last_activity' ;"
        cur.execute(st)
        rows = cur.fetchall()
        la=rows[0][0]
    except KeyError as e :
         print("key error encountered or e=",e)
    con.close()
    return la

# Update Last activity
def updateLastActivity(val):
    #connection to sqlite db strava.db
    con = sqlite3.connect('strava.db')
    cur = con.cursor()

    try:
        st="UPDATE settings SET value = " + str(val) + " WHERE key='last_activity';"
        cur.execute(st)
        con.commit()
        print("Update Last activity with" ,val)
    except KeyError as e :
         print("key error encountered or e=",e)
    con.close()



# Add segmment into segments table
def addsegment(id, con):
    with open('strava_tokens.json') as json_file:
            strava_tokens = json.load(json_file)

    #connection to sqlite db strava.db
    #con = sqlite3.connect('strava.db')
    cur = con.cursor()

    url = "https://www.strava.com/api/v3/segments/"+id
    access_token = strava_tokens['access_token']

    r = requests.get(url + '?access_token=' + access_token)
    r = r.json()

    try:
        
        st="SELECT * from segments where ID = '"+id+"'"
        cur.execute(st)
        rows = cur.fetchall()
        if len(rows) == 0:
           print("Adding segment : ",id)
           st="""INSERT INTO segments (ID,name,activity_type,distance,average_grade,maximum_grade,elevation_high,elevation_low,total_elevation_gain,climb_category,city,state,country,private,starred) VALUES (? ,?, ?, ?, ?, ?, ?, ?, ?, ?,? ,?, ?, ?, ?)"""
           try:
               cur.execute(st,(r['id'],r['name'],r['activity_type'],r['distance'],r['average_grade'],r['maximum_grade'],r['elevation_high'],r['elevation_low'],r['total_elevation_gain'],r['climb_category'],r['city'],r['state'],r['country'],r['private'],r['starred']))
               con.commit()
           except Exception as e :
               print("Error encountered while adding segment e=",e)
        
    except KeyError as e :
         print("key error encountered or e=",e)


# add activity into activities table 
def addActivity(id):

    print("Pat Add  addactivity id=",id)

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

    aid=r['id']
    try: 
        name=r['name']
    except Exception:
        name=""    
    try: 
        distance=r['distance']
    except Exception:
        distance=0
    try:    
        moving_time=r['moving_time']
    except Exception:
        moving_time=0    
    try:
        elapsed_time=r['elapsed_time']
    except Exception:  
        elapsed_time=0  
    try:        
        elevation=r['total_elevation_gain']
    except Exception:
        elevation=0
    try:
        athlete=r['athlete']['id']
    except Exception:  
        athlete=""  
    try:
        type=r['type']
    except Exception:
        type=""
    try:
        sport_type=r['sport_type']
    except Exception:
        sport_type=""
    try:
        workout_type=r['workout_type']
    except Exception:
        workout_type=""
    try:
        start_date_local=r['start_date_local']
    except Exception: 
        start_date_local=""   
    try:
        location_city=r['location_city']
    except Exception:
        location_city=""
    try:
        location_state=r['location_state']
    except Exception:
        location_state=""
    try:
        location_country=r['location_country']
    except Exception:
        location_country=""
    try:
        private=r['private']
    except Exception:
        private=0
    try:
        flagged=r['flagged']
    except Exception:
        flagged=0
    try:
        start_lat=r['start_latlng'][0]
    except Exception:
        start_lat=0
    try:
        start_lng=r['start_latlng'][1]
    except Exception:
        start_lng=0
    try:
        end_lat=r['end_latlng'][0]
    except Exception:
        end_lat=0
    try:
        end_lng=r['end_latlng'][0]
    except Exception:
        end_lng=0
    try:
        average_speed=r['average_speed']
    except Exception:
        average_speed=0
    try:
        max_speed=r['max_speed']
    except Exception:
        max_speed=0
    try: 
        average_cadence=r['average_cadence']
    except Exception:
        average_cadence=0 
    try:
        average_temp=r['average_temp']
    except Exception:
        average_temp=0
    try:
        average_watts=r['average_watts']
    except Exception:
        average_watts=0
    try:
        elevation_high=r['elev_high']
    except Exception:
        elevation_high=0
    try:
        elevation_low=r['elev_low']
    except Exception:
        elevation_low=0
    try:
        calories=r['calories']
    except Exception:
        calories=0
    try:
        description=r['description']
    except Exception:
        description=""
    try:
        gear_name=r['gear']['name']
    except Exception:
        gear_name=""
    try:
        gear_distance=r['gear']['converted_distance']
    except Exception:
        gear_distance=0
    try:
        device=r['device_name']
    except Exception:
        device=""
    print("Add activities", id)
    st = """INSERT INTO activities (ID,name,distance,moving_time,elapsed_time,elevation,athlete,type,sport_type,workout_type,start_date_local,location_city,location_state,location_country,private,flagged,start_lat,start_lng,end_lat,end_lng,average_speed,max_speed,average_cadence,average_temp,average_watts,elevation_high,elevation_low,description,calories,gear_name,gear_distance,device) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    try:
        cur.execute(st, (aid,name,distance,moving_time,elapsed_time,elevation,athlete,type,sport_type,workout_type,start_date_local,location_city,location_state,location_country,private,flagged,start_lat,start_lng,end_lat,end_lng,average_speed,max_speed,average_cadence,average_temp,average_watts,elevation_high,elevation_low,description,calories,gear_name,gear_distance,device))
    except sqlite3.IntegrityError as e:
            print("activitiy already exists", e, " ", st)
    
    con.commit()
    con.close()


# add segment_efforts from an activity into segment_efforts table 
def gse(id):
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

    for s in r['segment_efforts']:
        seid = str(s['id'])
        sid = str(s['segment']['id'])
        name = s['name']
        distance = str(s['segment']['distance'])
        athlete_id = str(s['athlete']['id'])
        moving_time = str(s['moving_time'])
        elapsed_time = str(s['elapsed_time'])
        try:
            average_watts = str(s['average_watts'])
        except KeyError:
            average_watts = "0"
        average_grade = str(s['segment']['average_grade'])
        try:
            elevation = str(round(s['segment']['elevation_high']-s['segment']['elevation_low']))
        except TypeError:
            elevation = ""
        start_date_local = str(s['start_date_local'])

        if elevation != "":
            print("Add effort for segment ", name, " ", seid)
            addsegment(sid, con)
                #st="INSERT INTO segment_efforts (ID,segment_ID,activity_ID,segment_name,segment_distance,athlete_ID,moving_time,elapsed_time,average_watts,average_rate,elevation,start_date_local) VALUES (" + seid + "," + sid + "," + id + ", + \"%s\" + ," + distance + "," + athlete_id + "," + moving_time + "," + elapsed_time + "," + average_watts + "," + average_grade + "," + elevation + "," + start_date_local+")"
            st = """INSERT INTO segment_efforts (ID,segment_ID,activity_ID,segment_name,segment_distance,athlete_ID,moving_time,elapsed_time,average_watts,average_rate,elevation,start_date_local) VALUES (?,?,?,?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            try:
                cur.execute(st, (seid, sid, id, name, distance, athlete_id, moving_time, elapsed_time, average_watts,average_grade,elevation,start_date_local))
            except sqlite3.IntegrityError as e:
                print("segment effort already added or ee=", e, " ", st)
    
    con.commit()
    con.close()

# get all segments effort for a segment
def retrieve_segment_efforts(sid):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    st="SELECT elapsed_time,start_date_local,elevation,segment_distance,average_rate FROM segment_efforts WHERE segment_ID =  '" + sid + "' ORDER by start_date_local ;"
    cur.execute(st)
    rows = cur.fetchall()
    con.close()
    #print(rows)
    return(rows)

# get all segments 
def retrieve_segments(pattern, like,starred):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    
    if pattern != "" : 
        if like == "like":
            pattern="%"+pattern+"%"  
        st="SELECT name,id FROM segments where name " + like + " '" + pattern + "' "
        if starred == "true":
            st += " AND starred = 1"
    else :
        st="SELECT name,id FROM segments"
        if starred == "true":
            st += " WHERE starred = 1"
    st +=  ";" 
    cur.execute(st)
    rows = cur.fetchall()
    con.close()
    return(rows)

# get all ascensions >= pct pourcentage 
def retrieve_ascensions(pct):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    st="SELECT segment_distance,segment_efforts.moving_time,segment_efforts.elevation,segment_efforts.start_date_local from segment_efforts INNER JOIN segments ON segment_efforts.segment_ID=segments.ID INNER JOIN activities ON segment_efforts.activity_ID=activities.ID where average_rate >= "+str(pct)+" AND type='Ride' AND starred=1;"     
    cur.execute(st)
    rows = cur.fetchall()
    con.close()
    return(rows)

# get all activities 
def retrieve_activities():
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    st="SELECT name,ID,distance,moving_time,elevation,average_speed,max_speed,average_cadence,average_temp,gear_name,gear_distance,start_date_local from  activities where type = 'Ride' and sport_type='Ride'and distance>5000 and elevation > 10 and average_speed>1.66;"    
    cur.execute(st)
    rows = cur.fetchall()
    con.close()
    return(rows)
