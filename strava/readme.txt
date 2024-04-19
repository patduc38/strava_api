# to get activities 
!! the instructions below was the very first way to synchronize strava activities. This step is now much more simple and is done from the web app itself

#>:~/strava_api/strava $ cd /home/pi/strava_api/strava
#>:~/strava_api/strava $ source strava_python-env/bin/activate
(strava_python-env) #>:python get_all_activities_segments.py treat
(strava_python-env) #>:~/strava_api/strava $ python retrieve.py

# to launch server

export DEBUG=True
nohup python run.py &
