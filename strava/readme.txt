# to get activities 

pi@raspberrypi:~/strava_api/strava $ cd /home/pi/strava_api/strava
pi@raspberrypi:~/strava_api/strava $ source strava_python-env/bin/activate
(strava_python-env) pi@raspberrypi:python get_all_activities_segments.py treat
(strava_python-env) pi@raspberrypi:~/strava_api/strava $ python retrieve.py

# to launch server

export DEBUG=True
nohup python run.py &
