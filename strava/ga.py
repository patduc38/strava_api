import requests
import json
import sqlite3
from datetime import datetime
from datetime import timezone

# true if activity has been treated 
def isActivityPresent(a):
    #connection to sqlite db strava.db
    con = sqlite3.connect('strava.db')
    cur = con.cursor()

    try:
        st="SELECT * FROM activities WHERE ID =  '"+str(a)+"' ;"
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
def readLastActivity(uid):
    #connection to sqlite db strava.db
    con = sqlite3.connect('strava.db')
    cur = con.cursor()
    la=0

    try:
       # st="SELECT value  FROM settings WHERE key =  'last_activity' ;"
        st="SELECT last_activity_segment FROM strava_users WHERE ID = '" + str(uid) + "' ;"
        cur.execute(st)
        rows = cur.fetchall()
        con.close()
        if len(rows) > 0 :
            rv=rows[0][0]
            la=datetime.fromisoformat(rv[:-1]).astimezone(timezone.utc).timestamp()
    except KeyError as e :
         print("key error encountered or e=",e)
    return la

# Update Last activity
def updateLastActivity(val,uid):
    #connection to sqlite db strava.db
    con = sqlite3.connect('strava.db')
    cur = con.cursor()
    try:
        st="UPDATE strava_users SET last_activity_segment = '" + str(val) + "' WHERE ID ='" +str(uid) + "';"
        cur.execute(st)
        con.commit()
        con.close()
        print("Update Last activity with" ,val)
    except Exception as e :
         print("Exception encountered or e=",e)

# Update activity with summary
def updateActivityPolyline(summary_polyline,aid):
    #connection to sqlite db strava.db
    con = sqlite3.connect('strava.db')
    cur = con.cursor()
    try:
        st="UPDATE activities SET summary_polyline = '" + str(summary_polyline) + "' WHERE ID ='" +str(aid) + "';"
        cur.execute(st)
        con.commit()
        con.close()
        print("Update Last activity ok")
    except Exception as e :
         print("Exception encountered or e=",e)

def isSegmentPresent(s):
    #connection to sqlite db strava.db
    con = sqlite3.connect('strava.db')
    cur = con.cursor()

    try:
        st="SELECT * FROM segments WHERE ID =  '"+str(s)+"' ;"
        cur.execute(st)
        rows = cur.fetchall()
        con.close()
        if len(rows) > 0:
            return True
    except KeyError as e :
        print("key error encountered or e=",e)
        con.close()
    return False

# Add segmment into segments table
def addsegment(sid, con,access_token=''):

    #first check thatt segment is not yet present 
    if isSegmentPresent(sid):
        return
    if access_token == '' :
        with open('strava_tokens.json') as json_file:
            strava_tokens = json.load(json_file)
        access_token = strava_tokens['access_token']
    #connection to sqlite db strava.db
    #con = sqlite3.connect('strava.db')
    cur = con.cursor()

    url = "https://www.strava.com/api/v3/segments/"+sid

    r = requests.get(url + '?access_token=' + access_token)
    r = r.json()

    print("Adding segment : ",sid)
    st="""INSERT INTO segments (ID,name,activity_type,distance,average_grade,maximum_grade,elevation_high,elevation_low,total_elevation_gain,climb_category,city,state,country,private,starred) VALUES (? ,?, ?, ?, ?, ?, ?, ?, ?, ?,? ,?, ?, ?, ?)"""
    try:
        city=r.get('city') 
        if city == None:
          city=""
        state=r.get('state')
        if state == None:
          state=""
        country=r.get('country')
        if country == None:
          country=""

        cur.execute(st,(r['id'],r['name'],r['activity_type'],r['distance'],r['average_grade'],r['maximum_grade'],r['elevation_high'],r['elevation_low'],r['total_elevation_gain'],r['climb_category'],city,state,country,r['private'],r['starred']))
        con.commit()
    except Exception as e :
               print("Error encountered while adding segment e=",e)

# Add segmment into segments table
def addsegmentFromEffort(sid,ses, con,access_token=''):

    #first check thatt segment is not yet present 
    if isSegmentPresent(sid):
        return
   
    cur = con.cursor()

    url = "https://www.strava.com/api/v3/segments/"+sid

    print("Adding segment : ",sid)
    st="""INSERT INTO segments (ID,name,activity_type,distance,average_grade,maximum_grade,elevation_high,elevation_low,total_elevation_gain,climb_category,city,state,country,private,starred) VALUES (? ,?, ?, ?, ?, ?, ?, ?, ?, ?,? ,?, ?, ?, ?)"""
    try:
        city=ses.get('city') 
        if city == None:
          city=""
        state=ses.get('state')
        if state == None:
          state=""
        country=ses.get('country')
        if country == None:
          country=""
        cur.execute(st,(ses['id'],ses['name'],ses['activity_type'],ses['distance'],ses['average_grade'],ses['maximum_grade'],ses['elevation_high'],ses['elevation_low'],ses['elevation_high']-ses['elevation_low'],ses['climb_category'],city,state,country,ses['private'],ses['starred']))
        con.commit()
    except Exception as e :
               print("Error encountered while adding segment e=",e)

# add activity into activities table 
def addActivity(id,access_token=''):

    #connection to sqlite db strava.db
    con = sqlite3.connect('strava.db')
    cur = con.cursor()

    st="select * from activities where ID="+ str(id) + " AND athlete=1758959"

    try:
        cur.execute(st)
    except sqlite3.IntegrityError as e:
        raise Exception("error while adding activitiy err="+str(e))

    rows = cur.fetchall()
    if len(rows)>0 :
        raise Exception(f"activity {id} already exist")

    # Get the tokens from file to connect to Strava
    if access_token=='' :
        with open('strava_tokens.json') as json_file:
            strava_tokens = json.load(json_file)
        access_token = strava_tokens['access_token']

    url = "https://www.strava.com/api/v3/activities/"+id

    
    r = requests.get(url + '?access_token=' + access_token)
    r = r.json()

    try:
        aid=r['id']
    except Exception:
        raise Exception("response rc is"+r)
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
        _type=r['type']
    except Exception:
        _type=""
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
    try:
        summary_polyline=r['map']['summary_polyline']
    except Exception:
        summary_polyline=""

    print("Add activities", id)
    st = """INSERT INTO activities (ID,name,distance,moving_time,elapsed_time,elevation,athlete,type,sport_type,workout_type,start_date_local,location_city,location_state,location_country,private,flagged,start_lat,start_lng,end_lat,end_lng,average_speed,max_speed,average_cadence,average_temp,average_watts,elevation_high,elevation_low,description,calories,gear_name,gear_distance,device,summary_polyline) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    try:
        cur.execute(st, (aid,name,distance,moving_time,elapsed_time,elevation,athlete,_type,sport_type,workout_type,start_date_local,location_city,location_state,location_country,private,flagged,start_lat,start_lng,end_lat,end_lng,average_speed,max_speed,average_cadence,average_temp,average_watts,elevation_high,elevation_low,description,calories,gear_name,gear_distance,device,summary_polyline))
    except sqlite3.IntegrityError as e:
            print("activitiy already exists", e, " ", st)
    
    con.commit()
    con.close()
    return r

def getActivitySegments(activity,access_token=''):
    if access_token=='' :
        with open('strava_tokens.json') as json_file:
            strava_tokens = json.load(json_file)
        access_token = strava_tokens['access_token']
    
    url = "https://www.strava.com/api/v3/activities/"+str(activity)
    url=url + '?access_token=' + access_token
    r = requests.get(url)
    r = r.json() 

    if  isinstance(r, dict)  :
        print("Pat Add in getActivitySegment=0")
        if ('message' in r):
            print("Pat Add in getActivitySegment=1")
            if (r['message'] == 'Rate Limit Exceeded' ) :
                return("quota exceeded")             
            if r['message'] == 'Authorization Error':
                return("refresh token expected")
    row=[]          
    for s in r['segment_efforts']:
        seid = str(s['id'])
        sid = str(s['segment']['id'])
        name = s['name']
        distance = str(s['segment']['distance'])
        athlete_id = str(s['athlete']['id'])
        moving_time = str(s['moving_time'])
        elapsed_time = str(s['elapsed_time'])
        starred = str(s['segment']['starred'])
        private=str(s['segment']['private'])
        average_grade = str(s['segment']['average_grade'])
        try:
            elevation = str(round(s['segment']['elevation_high']-s['segment']['elevation_low']))
        except TypeError:
            elevation=""

        if elevation != "" and abs(s['segment']['average_grade'])>4 and s['segment']['distance']>1000:
            row.append([sid,name,seid,distance,moving_time,average_grade])
    
    return(row)
           
def getActivityStreams(activity_ID,access_token=''):
    if access_token=='' :
        with open('strava_tokens.json') as json_file:
            strava_tokens = json.load(json_file)
        access_token = strava_tokens['access_token']

    url = "https://www.strava.com/api/v3/activities/"+activity_ID+"/streams?keys=distance&key_by_type=true"
    url = "https://www.strava.com/api/v3/segment_efforts/3251152918477905464/streams?keys=time,altitude,distance&key_by_type=true"
    
    r = requests.get(url + '&access_token=' + access_token)
    r = r.json()
    print("Pat Add r=",r," url=",url)

def getActivitySegmentEfforts(activity_id,access_token=''):
    if access_token=='' :
        with open('strava_tokens.json') as json_file:
            strava_tokens = json.load(json_file)
        access_token = strava_tokens['access_token']
    
    url = "https://www.strava.com/api/v3/activities/"+str(activity_id)
    url=url + '?access_token=' + access_token
    r = requests.get(url)
    r = r.json() 
    print ("Pat Add debug", r)
    if  isinstance(r, dict)  :
        if ('message' in r) :
            if r['message'] == 'Rate Limit Exceeded' :
                return("quota exceeded")
            if r['message'] == 'Authorization Error':
                return("refresh token expected")
    se=[]          
    for s in r['segment_efforts']:
        seid = str(s['id'])
        avg_rate =  s['segment']['average_grade']
        dist =  s['segment']['distance']
        print ("Pat Add debug seid", seid, s['segment']['name'], avg_rate, dist)
        if avg_rate * dist > 7000 :
            se.append([seid,  s['segment']['name'], avg_rate, dist, s['segment']['elevation_high']-s['segment']['elevation_low']])
    print ("Pat Add debug", se)
    return se

def getSegmentEffortStreams(se_id, access_token=''):
    if access_token=='' :
        with open('strava_tokens.json') as json_file:
            strava_tokens = json.load(json_file)
        access_token = strava_tokens['access_token']
    url = "https://www.strava.com/api/v3/segment_efforts/"+str(se_id)+"/streams?keys=time,altitude,latlng&key_by_type=true&resolution=low"
    r = requests.get(url + '&access_token=' + access_token)
    r = r.json()
    print("Pat Add getSegmentEffortStreams",r)
    return r

def getSegmentEffortInfo(sid):   
    con = sqlite3.connect('strava.db')
    cur = con.cursor()

    try:
        st="SELECT segment_name,segment_distance,elevation,average_rate,start_date_local FROM segment_efforts WHERE ID = '" + str(sid) + "' ;"
        cur.execute(st)
        rows = cur.fetchall()
        con.close()
        print("Pat Add======>", rows,st)
        if len(rows) > 0 :
            a=[]
            for i in rows[0]:
                a.append(i)
            return a 
    except KeyError as e :
         print("key error encountered or e=",e)
    return []

def getSegmentStats(sid,aid,Month="",Year=""):
    con = sqlite3.connect('strava.db')
    cur = con.cursor()
    final=[]
    try:
        if Month == "":
            if Year == "" :
                current_year=current_year = datetime.now().year
                for y in range(current_year,current_year-8,-1):
                    st=f'select moving_time from segment_efforts where athlete_ID={aid} and segment_ID={sid} and STRFTIME("%Y", start_date_local)="{y}";'
                    print("Pat Add st=",st)
                    cur.execute(st)
                    rows = cur.fetchall()
                    a=[]
                    if len(rows) > 0 :
                        for row in rows:
                            a.append(row[0]) 
                    final.append(a)
                final.reverse()
                print("Pat Add final=",final)    
        # else:
        #     for i in  range(Month):
        #             if i<10:
        #                 m=f'0{i}'
        #             else:
        #                 m=i
        #             if Year == "" :
        #                 st=f'select moving_time from segment_efforts where athlete_ID={aid} and segment_ID={sid} and STRFTIME("%m", start_date_local)="{m}";'
        #                 print("Pat Add st=",st)
        #                 cur.execute(st)
        #                 rows = cur.fetchall()
        #                 print("Pat Add res=",res, "rows=",a)
        #             else :
        #                 st=f'select moving_time from segment_efforts where athlete_ID={aid} and segment_ID={sid} and STRFTIME("%m-%Y", start_date_local)="{m}-{Year}";'
        #                 print("Pat Add st=",st)
        #                 cur.execute(st)
        #                 rows = cur.fetchall()
                             
        #             if len(rows) > 0 :
        #                 a=[]
        #                 for row in rows:
        #                     a.append(row[0])
        #             res.append(a) 
        #             print("Pat Add res=",res, "rows=",a)          
                    
    except KeyError as e :
        print("key error encountered or e=",e)        
    #print("Pat Add res=",res,len(res))    
    return final

def buildDataFromSegmentEffortStreams(r):
      distances=r['distance']['data']
      times=r['time']['data']
      altitudes=r['altitude']['data']
      latlong=r['latlng']['data']
      cumuld=0
      cumuldd=0
      cumula=0
      cumulaa=0
      cumult=0
      cumultt=0
      prevelev=altitudes[0]
      result=[[0,altitudes[0],0,0,0,latlong[0][0],latlong[0][1]]]
      pointsList=[]
      pointsList.append([latlong[0][0],latlong[0][1]])
      if 0:
          url="https://api.elevationapi.com/api/Elevation?lat="+str(latlong[0][0])+"&lon="+str(latlong[0][1])+"&dataSet=IGN_1m"
          print("https://api.elevationapi.com/api/Elevation?lat="+str(latlong[0][0])+"&lon="+str(latlong[0][1])+"&dataSet=IGN_1m")
          r = requests.get(url,verify=False)
          r = r.json()
          prevelev=r['geoPoints'][0]['elevation']
      else:
          url="https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json?lon="+str(latlong[0][1])+"&lat="+str(latlong[0][0])+"&resource=ign_rge_alti_wld&delimiter=|&zonly=true"
          print("https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json?lon="+str(latlong[0][1])+"&lat="+str(latlong[0][0])+"&resource=ign_rge_alti_wld&delimiter=|&zonly=true")
          r = requests.get(url)
          r = r.json()
          prevelev=r['elevations'][0]
    
      print("Pat Add time=========",times)

      for i,d in enumerate(distances):              
             if i+1 < len(distances): 
                   pointsList.append([latlong[i+1][0],latlong[i+1][1]])
                   dx=distances[i+1]-d
                   ax=altitudes[i+1]-altitudes[i]
                   tx=times[i+1]-times[i]
                   #print("Pat add ax=",ax)
                   cumuld=cumuld+dx
                   cumuldd=cumuldd+dx
                   cumula=cumula+ax
                   cumulaa=cumulaa+ax
                   cumult=cumult+tx
                   cumultt=cumultt+tx
                   if cumuld>200 or i==(len(distances)-2):
                        if 0 : 
                            print("i=",i,"  =>   d=",cumuld," a=",cumula, " pct=", (cumula*100)/cumuld, "va=",(cumula/cumult)*3600)
                            url="https://api.elevationapi.com/api/Elevation?lat="+str(latlong[i+1][0])+"&lon="+str(latlong[i+1][1])+"&dataSet=IGN_1m"
                            print("https://api.elevationapi.com/api/Elevation?lat="+str(latlong[i+1][0])+"&lon="+str(latlong[i+1][1])+"&dataSet=IGN_1m")
                            r = requests.get(url,verify=False)
                            print("Pat Add",r)
                            r = r.json()
                            elev=r['geoPoints'][0]['elevation']
                            print("Pat Add",r,elev)
                        else: 
                            url="https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json?lon="+str(latlong[i+1][1])+"&lat="+str(latlong[i+1][0])+"&resource=ign_rge_alti_wld&zonly=true"
                            r = requests.get(url)
                            if r.status_code != 200:
                                url="https://api.elevationapi.com/api/Elevation?lat="+str(latlong[i+1][0])+"&lon="+str(latlong[i+1][1])+"&dataSet=IGN_1m"
                                r = requests.get(url,verify=False)
                                print("Pat Add",r)
                                if r.status_code != 200: 
                                    return 
                                r = r.json()
                                elev=r['geoPoints'][0]['elevation']
                            else:     
                                r = r.json()
                                elev=r['elevations'][0]
                        diffelev=elev-prevelev
                        prevelev=elev
                        pct=(diffelev/cumuld)*100
                        print("Pat Add pct=",pct)
                        point=[cumuldd,elev,pct,cumult,(cumula/cumult)*3600,latlong[i+1][0],latlong[i+1][1]]
                        result.append(point)

                        cumuld=0
                        cumula=0
                        cumult=0
      print("Pat cumulaa=",cumulaa,"cumuldd=",cumuldd,"cumultt=",cumultt,result)
      result.append(pointsList)
      return result

# add segment_efforts from an activity into segment_efforts table 
def gse(id,r=None,access_token='',):
    #connection to sqlite db strava.db
    con = sqlite3.connect('strava.db')
    cur = con.cursor()

    if r == None: 
        if access_token=='':
            # Get the tokens from file to connect to Strava
            with open('strava_tokens.json') as json_file:
                    strava_tokens = json.load(json_file)
            access_token = strava_tokens['access_token']

        url = "https://www.strava.com/api/v3/activities/"+id

        r = requests.get(url + '?access_token=' + access_token)
        r = r.json() 

        if  isinstance(r, dict)  :
                if ('messsage' in r) and  (r['message'] == 'Rate Limit Exceeded' ) :
                    return("quota exceeded")

    for s in r['segment_efforts']:
        seid = str(s['id'])
        sid = str(s['segment']['id'])
        name = s['name']
        distance = str(s['segment']['distance'])
        athlete_id = str(s['athlete']['id'])
        moving_time = str(s['moving_time'])
        elapsed_time = str(s['elapsed_time'])
        starred = str(s['segment']['starred'])
        private=str(s['segment']['private'])
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
            addsegmentFromEffort(sid, s['segment'], con, access_token)
                #st="INSERT INTO segment_efforts (ID,segment_ID,activity_ID,segment_name,segment_distance,athlete_ID,moving_time,elapsed_time,average_watts,average_rate,elevation,start_date_local) VALUES (" + seid + "," + sid + "," + id + ", + \"%s\" + ," + distance + "," + athlete_id + "," + moving_time + "," + elapsed_time + "," + average_watts + "," + average_grade + "," + elevation + "," + start_date_local+")"
            st = """INSERT INTO segment_efforts (ID,segment_ID,activity_ID,segment_name,segment_distance,athlete_ID,moving_time,elapsed_time,average_watts,average_rate,elevation,start_date_local) VALUES (?,?,?,?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            try:
                cur.execute(st, (seid, sid, id, name, distance, athlete_id, moving_time, elapsed_time, average_watts,average_grade,elevation,start_date_local))
            except sqlite3.IntegrityError as e:
                print("segment effort already added or ee=", e)
            try:
                st1 = """INSERT INTO segment_athlete (segment_ID,athlete_ID,private,starred) VALUES (?,?,?,?)"""
                cur.execute(st1, (sid, athlete_id, private, starred))
            except sqlite3.IntegrityError as e:
                print("segment effort already added in segment_athlete or ee=", e)
    con.commit()
    con.close()
    

# get all segments effort for a segment for user uid 
def retrieve_segment_efforts(sid,uid):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
       #SELECT elapsed_time,start_date_local,elevation,segment_distance,average_rate,polyline FROM segment_efforts INNER JOIN segment_info on segment_efforts.segment_ID = segment_info.segment_ID WHERE segment_efforts.segment_ID = 4815216;

    st="SELECT elapsed_time,start_date_local,elevation,segment_distance,average_rate,polyline FROM segment_efforts LEFT JOIN segment_info on segment_efforts.segment_ID = segment_info.segment_ID WHERE segment_efforts.segment_ID =  '" + str(sid) + "' AND athlete_ID='"+str(uid)+"' ORDER by start_date_local ;"
    cur.execute(st)
    rows = cur.fetchall()
    con.close()
    return(rows)

#get the most executed segment effort 
def retrieve_higher_segment_effort(uid):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    st="select  segment_ID,segment_name,count(*) from segment_efforts where athlete_ID="+ str(uid) + " AND average_rate > 5 group by segment_id ORDER  by count(*) DESC limit 1"
    cur.execute(st)
    rows = cur.fetchall()
    con.close()
    if len(rows) > 0:
        return (rows[0][0],rows[0][1])
    else: 
        return (0,0)

# Update segment starred for a segment 
def updateSegmentStarred(val,sid,aid):
    #connection to sqlite db strava.db
    con = sqlite3.connect('strava.db')
    cur = con.cursor()

    try:
        st="UPDATE segment_athlete SET starred = '" + str(val) + "' WHERE segment_ID ='" +str(sid) + "' AND athlete_ID = '"+str(aid) + "';"
        cur.execute(st)
        con.commit()
        con.close()
        print("Update segment starred with" ,val)
    except KeyError as e :
         print("key error encountered or e=",e)

# get all segments 
def retrieve_segments(pattern, like,starred,uid):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    
    if pattern != "" : 
        if like == "like":
            pattern="%"+pattern+"%"  
        #select segments.ID,segment_athlete.athlete_ID from segments INNER JOIN segment_athlete on segments.ID=segment_athlete.segment_ID WHERE segment_athlete.athlete_ID=1758959'    
        st="SELECT segments.name,segments.id,segment_athlete.starred FROM segments INNER JOIN segment_athlete on segments.ID=segment_athlete.segment_ID  where segments.name " + like + " '" + pattern + "' AND segment_athlete.athlete_ID='"+str(uid)+"'"
        if starred == "true":
            st += " AND segment_athlete.starred = 1"
    else :
        st="SELECT segments.name,segments.id,segment_athlete.starred FROM segments INNER JOIN segment_athlete on segments.ID=segment_athlete.segment_ID WHERE segment_athlete.athlete_ID='"+str(uid)+"'"
        if starred == "true":
            st += " AND segment_athlete.starred = 1"
    st +=  ";" 
    cur.execute(st)
    rows = cur.fetchall()
    con.close()
    return(rows)

# get all ascensions >= pct pourcentage  for user uid
def get_ascensions(pct,uid,starred=False):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    if starred :
        starstring = " AND segment_athlete.starred='True'" 
    else :
        starstring = " "
    #st="SELECT segment_distance,segment_efforts.moving_time,segment_efforts.elevation,segment_efforts.start_date_local from segment_efforts INNER JOIN segments ON segment_efforts.segment_ID=segments.ID INNER JOIN activities ON segment_efforts.activity_ID=activities.ID where average_rate >= "+str(pct)+" AND type='Ride' AND starred=1 AND athlete_ID='"+str(uid)+"';"     
    st="SELECT segment_distance,segment_efforts.moving_time,segment_efforts.elevation,segment_efforts.start_date_local,segment_efforts.segment_name,segments.starred,activity_ID from segment_efforts INNER JOIN segments ON segment_efforts.segment_ID=segments.ID INNER JOIN activities ON segment_efforts.activity_ID=activities.ID INNER JOIN segment_athlete ON segment_efforts.segment_ID=segment_athlete.segment_ID AND segment_efforts.athlete_ID=segment_athlete.athlete_ID  where average_rate >= "+str(pct)+ starstring+ " AND type='Ride' AND segment_distance >= 3000 AND segment_efforts.athlete_ID='"+str(uid)+"';"     
    cur.execute(st)
    rows = cur.fetchall()
    if len(rows) == 0:
      starstring = " "
      st="SELECT segment_distance,segment_efforts.moving_time,segment_efforts.elevation,segment_efforts.start_date_local,segment_efforts.segment_name,segments.starred,activity_ID from segment_efforts INNER JOIN segments ON segment_efforts.segment_ID=segments.ID INNER JOIN activities ON segment_efforts.activity_ID=activities.ID INNER JOIN segment_athlete ON segment_efforts.segment_ID=segment_athlete.segment_ID AND segment_efforts.athlete_ID=segment_athlete.athlete_ID  where average_rate >= "+str(pct)+ starstring+ " AND type='Ride' AND segment_distance >= 3000 AND segment_efforts.athlete_ID='"+str(uid)+"';"     
      cur.execute(st)
      rows = cur.fetchall()
      
    con.close()
    return(rows)

# get last 3 ascensions with lenght > length (m) and % > pct.
# return starred ascensions except if there is no starred ascensions matching
def get_last_3_ascensions(length,pct,uid,starred=True):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    if starred :
        starstring = " AND segment_athlete.starred='True' " 
    else :
        starstring = " "
    #st="SELECT segment_distance,segment_efforts.moving_time,segment_efforts.elevation,segment_efforts.start_date_local from segment_efforts INNER JOIN segments ON segment_efforts.segment_ID=segments.ID INNER JOIN activities ON segment_efforts.activity_ID=activities.ID where average_rate >= "+str(pct)+" AND type='Ride' AND starred=1 AND athlete_ID='"+str(uid)+"';"     
    st="SELECT segment_efforts.segment_name,segment_distance,segment_efforts.moving_time,segment_efforts.elevation,segment_efforts.start_date_local from segment_efforts INNER JOIN segments ON segment_efforts.segment_ID=segments.ID INNER JOIN activities ON segment_efforts.activity_ID=activities.ID INNER JOIN segment_athlete ON segment_efforts.segment_ID=segment_athlete.segment_ID AND segment_efforts.athlete_ID=segment_athlete.athlete_ID  where segment_distance>" +str(length)+" and average_rate >= "+str(pct)+ starstring+ " AND type='Ride' AND segment_efforts.athlete_ID='"+str(uid)+"' ORDER by segment_efforts.start_date_local DESC LIMIT 3;"     
    cur.execute(st)
    rows = cur.fetchall()
    if len(rows) == 0:
       starstring = " "
       st="SELECT segment_efforts.segment_name,segment_distance,segment_efforts.moving_time,segment_efforts.elevation,segment_efforts.start_date_local from segment_efforts INNER JOIN segments ON segment_efforts.segment_ID=segments.ID INNER JOIN activities ON segment_efforts.activity_ID=activities.ID INNER JOIN segment_athlete ON segment_efforts.segment_ID=segment_athlete.segment_ID AND segment_efforts.athlete_ID=segment_athlete.athlete_ID  where segment_distance>"+str(length)+ " and average_rate >= "+str(pct)+ " AND type='Ride' AND segment_efforts.athlete_ID='"+str(uid)+"' ORDER by segment_efforts.start_date_local DESC LIMIT 3;"     
       cur.execute(st)
       rows = cur.fetchall() 
    con.close()
    return(rows)

def get_longest_activity_ascension(cur,aid, length,pct,uid,starred=False,nbraw=1):
    if starred :
        starstring = " AND segment_athlete.starred='True'" 
    else :
        starstring = " "
    st="SELECT segment_efforts.segment_name,segment_distance,segment_efforts.moving_time,segment_efforts.elevation,segment_efforts.start_date_local from segment_efforts INNER JOIN segments ON segment_efforts.segment_ID=segments.ID INNER JOIN activities ON segment_efforts.activity_ID=activities.ID INNER JOIN segment_athlete ON segment_efforts.segment_ID=segment_athlete.segment_ID AND segment_efforts.athlete_ID=segment_athlete.athlete_ID  where segment_distance>"+str(length)+ " AND average_rate >= "+str(pct)+starstring+ "AND segment_efforts.activity_ID = '"+ str(aid)+"' ORDER by segment_distance DESC LIMIT "+str(nbraw)+";"     
    cur.execute(st)
    rows = cur.fetchall()
    if len(rows) == 0:
        st="SELECT segment_efforts.segment_name,segment_distance,segment_efforts.moving_time,segment_efforts.elevation,segment_efforts.start_date_local from segment_efforts INNER JOIN segments ON segment_efforts.segment_ID=segments.ID INNER JOIN activities ON segment_efforts.activity_ID=activities.ID INNER JOIN segment_athlete ON segment_efforts.segment_ID=segment_athlete.segment_ID AND segment_efforts.athlete_ID=segment_athlete.athlete_ID where segment_distance>"+str(length)+" AND average_rate >= "+str(pct) + " AND segment_efforts.activity_ID = '"+ str(aid)+"' ORDER by segment_distance DESC LIMIT "+str(nbraw)+";"     
        cur.execute(st)
        rows = cur.fetchall()
        if len(rows) == 0:
            st="SELECT segment_efforts.segment_name,segment_distance,segment_efforts.moving_time,segment_efforts.elevation,segment_efforts.start_date_local from segment_efforts INNER JOIN segments ON segment_efforts.segment_ID=segments.ID INNER JOIN activities ON segment_efforts.activity_ID=activities.ID INNER JOIN segment_athlete ON segment_efforts.segment_ID=segment_athlete.segment_ID AND segment_efforts.athlete_ID=segment_athlete.athlete_ID  where average_rate >= "+str(pct) + " AND segment_efforts.activity_ID = '"+ str(aid)+"' ORDER by segment_distance DESC LIMIT "+str(nbraw)+";"     
            cur.execute(st)
            rows = cur.fetchall()
    if len(rows) != 0 :
        return rows[0]
    else : 
        return None

def get_last_3_ascensions_2(length,pct,uid,starred=False):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    
    #get last 3 acttivities 
    rows=get_last_3_activities(uid)
    return_rows=[]
    nbrow=1
    newraw=get_longest_activity_ascension(cur,str(rows[0][1]), length,pct,uid,starred,nbrow)

    if newraw != None:
        return_rows.append(newraw)
    else :
        return_rows.append([rows[0][0],None,None,None,rows[0][11]])
    
    #return  ('Domene - le mont', None, None, None, '2024-04-26T17:54:46Z')] 
    newraw=get_longest_activity_ascension(cur,str(rows[1][1]), length,pct,uid,starred,nbrow)
    if newraw != None:
        return_rows.append(newraw)
    else :
        return_rows.append([rows[1][0],None,None,None,rows[1][11]])    
    
    newraw=get_longest_activity_ascension(cur,str(rows[2][1]), length,pct,uid,starred,nbrow)
    if newraw != None:
        return_rows.append(newraw)
    else :
        return_rows.append([rows[2][0],None,None,None,rows[2][11]])
    con.close()
    print(return_rows)
    return(return_rows)

# get all activities for user uid
def get_ride_activities(uid,limit=None,offset=None):
    
    limitstring=""
    if limit != None :
        if offset==None: 
            offset=0
        limitstring=" Limit " + str(limit) +  " offset " + str(offset) + " "           

    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    st="SELECT name,ID,distance,moving_time,elevation,average_speed,max_speed,average_cadence,average_temp,gear_name,gear_distance,start_date_local,summary_polyline from  activities where type = 'Ride' and sport_type='Ride'and distance>5000 and elevation > 10 and average_speed>1.66 and athlete ='"+str(uid)+"' ORDER by start_date_local DESC "+limitstring+";"    
    cur.execute(st)
    rows = cur.fetchall()
    con.close()
    return(rows)

# get all activities for user uid. 
def get_all_activities(uid):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    st="SELECT name,ID,distance,moving_time,elevation,average_speed,max_speed,average_cadence,average_temp,gear_name,gear_distance,start_date_local,summary_polyline from  activities where athlete ='"+str(uid)+"' ORDER by start_date_local ASC;"    
    cur.execute(st)
    rows = cur.fetchall()
    con.close()
    return(rows)


# get all activities for user uid and strava type. 
# type syntax is 'Type in ("Walk","Run")
def get_activities_by_type(uid,type):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    st="SELECT name,ID,distance,moving_time,elevation,average_speed,max_speed,average_cadence,average_temp,gear_name,gear_distance,start_date_local,summary_polyline from  activities where "+type+" and athlete ='"+str(uid)+"' ORDER by start_date_local ASC;"    
    cur.execute(st)
    rows = cur.fetchall()
    con.close()
    return(rows)

# get all activities for user uid and strava type. 
# type syntax is 'Type in ("Walk","Run")
def get_activities_repartition(uid):
    bike=len(get_activities_by_type(uid,"type='Ride'"))
    walk=len(get_activities_by_type(uid,"type='Walk'"))
    run=len(get_activities_by_type(uid,"type='Run'"))
    hike=len(get_activities_by_type(uid,"type='Hike'"))
    total=len(get_all_activities(uid))
    other=total-(bike+walk+run+hike)
    return([bike,run,walk,hike,other])

# get last 3 activities for user uid
def get_last_3_activities(uid):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    st="SELECT name,ID,distance,moving_time,elevation,average_speed,max_speed,average_cadence,average_temp,gear_name,gear_distance,start_date_local,summary_polyline from  activities where type = 'Ride' and sport_type='Ride'and distance>5000 and elevation > 10 and average_speed>1.66 and athlete ='"+str(uid)+"' ORDER by start_date_local DESC limit 3;"    
    cur.execute(st)
    rows = cur.fetchall()
    con.close()
    return(rows)

# get all activities inthe provided interval for user uid
def get_activities_in_interval(uid,begin_date,end_date):
    con = sqlite3.connect('strava.db')
    cur = con.cursor() 
    st="SELECT name,ID,distance,moving_time,elevation,average_speed,max_speed,average_cadence,average_temp,gear_name,gear_distance,start_date_local,summary_polyline from  activities where type = 'Ride' and sport_type='Ride'and distance>5000 and elevation > 10 and average_speed>1.66 and athlete ='"+str(uid)+"' AND start_date_local>date('"+str(begin_date)+"') and start_date_local<date('"+str(end_date)+"');"    
    cur.execute(st)
    rows = cur.fetchall()
    con.close()
    return(rows)
# Users
def get_user(user_json):
    #connection to sqlite db strava.db
    con = sqlite3.connect('strava.db')
    cur = con.cursor()
    uid=''
    if type(user_json) is dict :
        uid=user_json.get('id')
    else :
        uid=str(user_json)
    try:
        st="SELECT id,email,user_name,refresh_token FROM strava_users WHERE id =  " + str(uid) + " ;"
        cur.execute(st)
        rows = cur.fetchall()      
    except KeyError as e :
         print("key error encountered or e=",e) 
         return None     
    if len(rows) == 0 :   
        st="""INSERT INTO strava_users (ID, user_name, first_name, last_name, created_at, last_activity_segment) VALUES (? ,?, ?, ?, ?,?)"""
        try:
            cur.execute(st,(user_json['id'],user_json['username'],user_json['firstname'],user_json['lastname'],user_json['created_at'],'0'))
            con.commit()
            st="SELECT id,email,user_name,refresh_token FROM strava_users WHERE id =  "+str(uid)+" ;"
            cur.execute(st)
            rows = cur.fetchall()    
            if len(rows) == 0 :
                print("Error encountered while adding user e=",e)
                return None
        except Exception as e :
            print("Error encountered while adding user e=",e)
            return None

    con.close()
    return rows[0]

def update_refresh_token(uid,refresh_token): 
    con = sqlite3.connect('strava.db')
    cur = con.cursor()
    st="""UPDATE strava_users SET refresh_token = ? WHERE ID = ? """
    try:   
        cur.execute(st,(str(refresh_token),str(uid)))
        con.commit()
    except KeyError as e :
            print("Error encountered while updating user refresh_token, e=",e)
    con.close()       
