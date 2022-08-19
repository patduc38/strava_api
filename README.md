# strava_api

This is a very dirty code to connect to strava API to collect my info (the goal will be to compute additional statistic from these raw data) 

- first we need to generate a token

Enter the following URL in your browser

http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all

you will be redirected to strava auth site, click on authorize. Then you are redirected to a localhost url hich can't be reach, but anyway, the important information is in the url. Copy the code in the get_initial_token.py , you will also have to replace your client id in that file. 

![image](https://user-images.githubusercontent.com/16572059/185616908-a010eec9-af54-44b1-b247-64294650362c.png)


Note:  you can get your client id get from strava : https://www.strava.com/settings/api

Then run 

python get_initial_token.py 

it will generate strava_tokens.json file that will be used to access the url 

- regenerate token on expiration 

the token is available only for a few minutes, then  you need to regenerate *strava_tokens.json* :

python retireve.py 


- then you can display all your activities id 

python get_all_activities1.py > activities 

- or stored these activities in sqlite *strava.db * 

python get_all_activities.py  (it will populate segments_efforts sqlite tabble) 

- to populate strava.db sqlite db with all segments you visited you can call 

python get_all_segments_from_activities.py   (it will activities from *activities* file, extract segments forom each activity and populate strava.db segments table if it find new segments) 

- Once you have these data you can query sqlite db and build some statistics obased on your data 

basic exxample: 

#> echo "$(sqlite3 strava.db 'select SUM(elevation) from segment_efforts where start_date_local like "2022-%" AND average_rate > 9;')/$ echo "(sqlite3 strava.db 'select SUM(moving_time) from segment_efforts where start_date_local like "2022-%" AND average_rate > 9 ;')*3600"|bc -l 
1021.52172846600744253200

It corresponds to the elvation by hour for all efforts on segments with a average rate > 9% in 2022 



