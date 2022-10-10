import requests
import json
import sys 
#from pandas.json import json_normalize
import  pandas
import csv
import ga

treatLast=False
if len(sys.argv) == 2 :
    treatLast = True
try: 
    n=int(ga.readLastActivity())
    print("Last Activity seen is ",n)
except Exception as e:
    print("Can't get lastActivity",e)

# Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
# Loop through all activities
url = "https://www.strava.com/api/v3/activities/"
access_token = strava_tokens['access_token']
# Get first page of activities from Strava with all fields
p=1
a=[]
while 1 : 
    r = requests.get(url + '?access_token=' + access_token+"&per_page=200&page="+ str(p))
    p=p+1
    r = r.json()
    if not r : 
        break
    for s in  r :
        if treatLast == True: 
            if s['id'] > n :
                 a.append(str(s['id']))
        else :
            if not ga.isActivityPresent(s['id']) :
                a.append(str(s['id']))
   
a.reverse()

for ac in a :
    print("Treat Activity=",ac)
    try : 
        print("Pat Add about to add=",ac)
        ga.addActivity(ac)
        print("Pat Add normaly it should be ok")
        ga.gse(ac)
        ga.updateLastActivity(ac)
    except Exception as e:    
        print("An error was encountered with activity:", ac," ",e)



