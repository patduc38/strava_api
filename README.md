Strava Dasboard 
A flask based server to display analyse Strava data

## Introduction
The Strava dashboard tool aims to use your strava tool to display your own dashboard. It provides some functionalities that are available only in the strava premium version but also some additional functionalities that are not available from strava web/mobile app. 

## Installation/access
if you want to give it a try, you can send me a message (patduc38@gmail.com) and I'll provide you the url of a running site. Though fully functional, this is a very first experimental deployment running on a modest raspberry device so it should not be able to face hundred/thousand of simultaneous connections, it's why I don't publish the server url    
This iniital version is on french only, I may add english langage as well in the next version

**TODO: explain hos to setup the server**  
You can also install the server in your own local environment. This operation is not yet documented. Basically you have to setup the configuration of the internal sqlite db and start the flask application. 

## login (with your username/password or via strava) 
![Capture](https://github.com/patduc38/strava_api/assets/16572059/5e592a77-81b1-4a7f-b84d-1db0b6c9f4b7)

## Dashboard 
if you browse the "Dashboard" section, you get a summary of your strava activities (Ride only so far). Various statistics information are available such as info regarding your activities, your climbs and also trends for the past week, month or year. You also get a summary of your last 3 activities and climbs.  

![Capture1](https://github.com/patduc38/strava_api/assets/16572059/f4d1ad7f-693f-45d6-a8d6-e61f56b446d6)

## Activities display 
if you browse the "Activités" section, a table of all your activities is displayed with  related information (distance, time, elevation...). If you click on an activity, the corresponding map is displayed 

![Capture2](https://github.com/patduc38/strava_api/assets/16572059/a5f65b80-1753-4cb0-a8e5-0f156dd7bc94)

## Climb display 
if you browse the "Ascensions" section, you get all strava segments corresponding to your climbs. You can select each segment and display related statistics (elevation, distance numnber of escalation, time..) and a graph of all climbs of that segment is displayed with additional information such as best and worse time or average time. 

![Capture3](https://github.com/patduc38/strava_api/assets/16572059/19f3e42b-bd1b-4acc-810a-2c1b17f0e36f)

## Graph 
if you browse "Statistiques" section, you get a graph displaying metrics (distance, elevation, number) of your activities. You can select different years to compare the activities in a graphical way

![Capture5](https://github.com/patduc38/strava_api/assets/16572059/3d8daf69-13bb-424f-a0c7-af2eb24839cd)

## Heatmap 
if you browse "Heatmap", a map with all your activities (Rides in blue, walks in red) is displayed 

![Capture6](https://github.com/patduc38/strava_api/assets/16572059/069c8d9c-959f-4fcf-b2aa-e2c7987204f9)

## Synchronization with strava
in the "Sync" section, you can synchronize with strava and retrieve your last strava activities.The first synchronization could be long depending on the number of activities you have on strava. There is some quota restrictions to access the strava Api, so depending on the number of activities you have on strava and the number of requests already sent to strava API, you may not get all your activities. In that case you have to retry later (2 types of quota are setup for the strava api, per day and every 15 minutes). 
