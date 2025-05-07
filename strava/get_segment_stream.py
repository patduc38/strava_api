import requests
import json
#from pandas.json import json_normalize
import  pandas
import csv
import ga
import sys 

if len(sys.argv) >1 : 
      se=sys.argv[1] 
else :
      se=3249843914511902138

# Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
# Loop through all activities
url = "https://www.strava.com/api/v3/segment_efforts/"+str(se)+"/streams?keys=time,altitude,latlng&key_by_type=true&resolution=low"
access_token = strava_tokens['access_token']

try:

      access_token = strava_tokens['access_token']
      r = requests.get(url + '&access_token=' + access_token)
      print("Pat add d=",json.dumps(r.json()))
      y = json.loads(json.dumps(r.json()))
      print("Pat Add json=", y)

      r = r.json()
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
      result=[]

      url="https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json?lon="+str(latlong[0][1])+"&lat="+str(latlong[0][0])+"&resource=ign_rge_alti_wld&zonly=true"
      r = requests.get(url)
      r = r.json()
      print("Pat Add initial elev",json.dumps(r))
      prevelev=r['elevations'][0]

      for i,d in enumerate(distances): 
             if i+1 < len(distances): 
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
                   if cumuld>450 :
                        print("i=",i,"  =>   d=",cumuld," a=",cumula, " pct=", (cumula*100)/cumuld, "va=",(cumula/cumult)*3600)
                        url="https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json?lon="+str(latlong[i+1][1])+"&lat="+str(latlong[i+1][0])+"&resource=ign_rge_alti_wld&zonly=true"
                        r = requests.get(url)
                        r = r.json()
                        print("Pat Add",r)
                        elev=r['elevations'][0]
                        diffelev=elev-prevelev
                        prevelev=elev
                        pct=(diffelev/cumuld)*100
                        print("Pat Add pct=",pct)
                        point=[cumuldd,cumuld,pct]
                        result.append(point)

                        cumuld=0
                        cumula=0
                        cumult=0
      print("Pat cumulaa=",cumulaa,"cumuldd=",cumuldd,"cumultt=",cumultt,result)

#       print("Pat get stream distance=",distances) 
#       print("Pat get stream times=",times) 
#       print("Pat get stream altitudes=",altitudes) 

except Errors as e:
        print("there is an error")
