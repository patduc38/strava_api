# strava_api

This is a very doirty code to connect to strava API to collect my info (the goal will be to compute additional statistic from these raw data) 

- first we need to generate a token

edit retrieve.py and copy your strava client_secret you get from strava : https://www.strava.com/settings/api, then run 

python retireve.py 

it will generate a token_file *strava_tokens.json*

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



