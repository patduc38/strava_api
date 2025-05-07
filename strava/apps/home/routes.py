# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from signal import sigtimedwait
from array import *
from apps.home import blueprint
from flask import render_template, request,url_for, redirect, session, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from datetime import date, timedelta
import requests
import ga
import json
import os
import urllib


STRAVA_CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

def refresh_token(uid):
    user=ga.get_user(uid)
    response = requests.post(
    url = 'https://www.strava.com/oauth/token',
    data = {
            'client_id': STRAVA_CLIENT_ID,
            'client_secret': STRAVA_CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': user[3]
            }
    )
    # Save response as json in new variable
    new_strava_tokens = response.json()
    session['token']=new_strava_tokens['access_token']

def exchange_token(code):
    strava_request = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': STRAVA_CLIENT_ID,
            'client_secret': STRAVA_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
    )
    return jsonify(strava_request.json())

@blueprint.route('/strava_authorize')
def strava_authorize():
    params = {
        'client_id': STRAVA_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'read_all,activity:read_all'
    }
    return redirect('{}?{}'.format(
        'https://www.strava.com/oauth/authorize',
        urllib.parse.urlencode(params)
    ))

@blueprint.route('/strava_token')
def strava_token():
    code = request.args.get('code')
    if not code:
        return Response('Error: Missing code param', status=400)
    return exchange_token(code)


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/ascensions')
@blueprint.route('/ascensions.html')
@login_required
def ascensions():
    pattern=request.args.get('pattern')
    if pattern == None :
        pattern=""
    mode=request.args.get('mode')
    if mode == None:
        mode="like"
    starred=request.args.get('starred')
    if starred == None:
        starred="false"

    datasegments = ga.retrieve_segments(pattern,mode,starred,session['uid'])
    ids = [row[1] for row in datasegments]
    names = [row[0] for row in datasegments]
    higher_segment=ga.retrieve_higher_segment_effort(session['uid'])
    data = ga.retrieve_segment_efforts(higher_segment[0],session['uid'])
    labels = [row[1] for row in data]
    values = [row[0] for row in data]
    return render_template('home/ascensions.html', segment='ascensions',higher_segment=higher_segment[0],higher_segment_name=higher_segment[1],datasegments=datasegments,ids=ids,names=names,labels=labels, values=values,pattern=pattern,mode=mode,starred=starred)

@blueprint.route('/segment_effort')
@blueprint.route('/segment_effort.html')
@login_required
def segment_effort():
    seid=request.args.get('seid')
    r=ga.getSegmentEffortStreams(seid,session['token'])
    if isinstance(r, dict)  :
      if 'message' in r and  r['message'] == 'Rate Limit Exceeded':
        return render_template('home/strava_auth_err.html', user=user)
      if 'message' in r and r['message'] == 'Authorization Error':
        refresh_token(session['uid'])
        r=ga.getSegmentEffortStreams(seid,session['token'])
    info=ga.getSegmentEffortInfo(seid)
    ose=ga.buildDataFromSegmentEffortStreams(r)
    return render_template('home/segment_effort.html', segment='segment_effort', one_segment_effort=ose, segment_info=info)

blueprint.route('/listactivities', methods = ['GET'])
@blueprint.route('/listactivities.html', methods = ['GET'])
def listactivities():
    # if count is in the args list then we return the number of activities 
    count=request.args.get('count')
    if count != None :
        data=ga.get_ride_activities(session['uid'])
        return jsonify(len(data))
    
    limit=request.args.get('limit')
    if limit == None :
        limit==""
    offset=request.args.get('offset')
    if offset == None:
        offset=""
    
    data=ga.get_ride_activities(session['uid'], limit,offset)
    return jsonify(data) 

blueprint.route('/listsegments', methods = ['GET'])
@blueprint.route('/listsegments.html', methods = ['GET'])
@login_required
def listsegments():
    # if count is in the args list then we return the number of activities 
    activity=request.args.get('activity') 
    data=ga.getActivitySegments(activity,session['token'])
    if type(data) == str and data=="refresh token expected":
         refresh_token(session['uid'])
         data=ga.getActivitySegments(activity,session['token'])
    return jsonify(data) 

blueprint.route('/try', methods = ['GET'])
@blueprint.route('/try.html', methods = ['GET'])
def ptry():
    sid=request.args.get('sid') 
    if sid == None:
        sid=5855232
    sname=request.args.get('sname')     
    data=ga.getSegmentStats(sid,session['uid'])
    limit=request.args.get('limit')
    if limit == None :
        limit==""
    offset=request.args.get('offset')
    if offset == None:
        offset=""
    return render_template('home/try.html',data=data,sname=sname)

@blueprint.route('/segments')
@blueprint.route('/segments.html')
@login_required
def segments():
    activity=request.args.get('activity')
    if activity == None :
        activity=""
    return render_template('home/segments.html',segment='segments',activity=activity)


blueprint.route('/pat', methods = ['GET'])
@blueprint.route('/pat.html', methods = ['GET'])
def pat():
    limit=request.args.get('limit')
    if limit == None :
        limit==""
    offset=request.args.get('offset')
    if offset == None:
        offset=""
    count=len(ga.get_ride_activities(session['uid'])) 
    return render_template('home/pat.html',limit=limit,offset=offset,count=count)

blueprint.route('/dashboard')
@blueprint.route('/dashboard.html')
@login_required
def dashboard():
    pattern=request.args.get('pattern')
    if pattern == None :
        pattern=""
    mode=request.args.get('mode')
    if mode == None:
        mode="like"
    starred=request.args.get('starred')
    if starred == None :
        starred=True
    elif starred.lower() == "false" :
        starred=False
    else:
        starred= True
    
    aseg=ga.getActivityStreams("11967430186","")
    activities = ga.get_ride_activities(session['uid'])
    activities_type=ga.get_activities_repartition(session['uid'])
    ascensions =  ga.get_ascensions(5,session['uid'],False)
    last3activities = json.dumps([row[0:13] for row in ga.get_last_3_activities(session['uid'])])
    last3ascensions = json.dumps([row[0:6] for row in ga.get_last_3_ascensions_2(1000,3,session['uid'])])
    now = date.today() 
    week_before = now  - timedelta(days=7)
    month_before = now -timedelta(days=30)
    year_before = now - timedelta(days=365)
    now = now + timedelta(days=1)
    two_week_before = week_before - timedelta(days=7)
    two_month_before= month_before -timedelta(days=30)
    two_year_before= year_before - timedelta(days=365)

    weekactivities=json.dumps([row[0:13] for row in ga.get_activities_in_interval(session['uid'],str(week_before),str(now))])
    weekbeforeactivities=json.dumps([row[0:13] for row in ga.get_activities_in_interval(session['uid'],str(two_week_before),str(week_before))])
    monthactivities=json.dumps([row[0:13] for row in ga.get_activities_in_interval(session['uid'],str(month_before),str(now))])
    monthbeforeactivities=json.dumps([row[0:13] for row in ga.get_activities_in_interval(session['uid'],str(two_month_before),str(month_before))])
    yearactivities=json.dumps([row[0:13] for row in ga.get_activities_in_interval(session['uid'],str(year_before),str(now))])
    yearbeforeactivities=json.dumps([row[0:13] for row in ga.get_activities_in_interval(session['uid'],str(two_year_before),str(year_before))])
    distance =[row[2] for row in activities]
    moving_time =[row[3] for row in activities]
    elevation =[row[4] for row in activities]
    average_speed=[row[5] for row in activities]
    max_speed=[row[6] for row in activities]
    average_cadence=[row[7] for row in activities]
    average_temp=[row[8] for row in activities]
    gear_name=[row[9] for row in activities]
    gear_distance=[row[10] for row in activities]
    activities_labels=[row[11] for row in activities]

    ascensions_distance=[row[0] for row in ascensions]
    ascensions_moving_time=[row[1] for row in ascensions]
    ascensions_elevation=[row[2] for row in ascensions]
    ascensions_labels=[row[3] for row in ascensions]
    ascensions_name=[row[4] for row in ascensions]
    ascensions_starred=[row[5] for row in ascensions]
    ascensions_activities_id=[row[6] for row in ascensions]

    return render_template('home/dashboard.html', segment='dashboard',wactivities=json.dumps(activities),activities_type=json.dumps(activities_type),yearactivities=yearactivities,yearbeforeactivities=yearbeforeactivities,monthactivities=monthactivities,monthbeforeactivities=monthbeforeactivities,weekactivities=weekactivities,weekbeforeactivities=weekbeforeactivities,last3ascensions=last3ascensions,last3activities=last3activities,distance=distance,moving_time=moving_time,elevation=elevation,average_speed=average_speed,max_speed=max_speed,average_cadence=average_cadence,average_temp=average_temp,gear_name=gear_name,gear_distance=gear_distance,activities_labels=activities_labels,ascensions_distance=ascensions_distance,ascensions_starred=ascensions_starred,ascensions_activities_id=ascensions_activities_id,ascensions_name=ascensions_name,ascensions_moving_time=ascensions_moving_time,ascensions_elevation=ascensions_elevation,ascensions_labels=ascensions_labels)

blueprint.route('/stats')
@blueprint.route('/stats.html')
@login_required
def stat():
    pattern=request.args.get('pattern')
    if pattern == None :
        pattern=""
    mode=request.args.get('mode')
    if mode == None:
        mode="like"
    starred=request.args.get('starred')
    if starred == None:
        starred="false"

    activities = ga.get_ride_activities(session['uid'])
    activities.reverse() #important activities should be ordered in ASC time and get-activities return them in DESC time
    ascensions =  ga.get_ascensions(5,session['uid'])
    distance =[row[2] for row in activities]
    moving_time =[row[3] for row in activities]
    elevation =[row[4] for row in activities]
    average_speed=[row[5] for row in activities]
    max_speed=[row[6] for row in activities]
    average_cadence=[row[7] for row in activities]
    average_temp=[row[8] for row in activities]
    gear_name=[row[9] for row in activities]
    gear_distance=[row[10] for row in activities]
    activities_labels=[row[11] for row in activities]

    ascensions_distance=[row[0] for row in ascensions]
    ascensions_moving_time=[row[1] for row in ascensions]
    ascensions_elevation=[row[2] for row in ascensions]
    ascensions_labels=[row[3] for row in ascensions]
    return render_template('home/stats.html', segment='stats',distance=distance,moving_time=moving_time,elevation=elevation,average_speed=average_speed,max_speed=max_speed,average_cadence=average_cadence,average_temp=average_temp,gear_name=gear_name,gear_distance=gear_distance,activities_labels=activities_labels,ascensions_distance=ascensions_distance,ascensions_moving_time=ascensions_moving_time,ascensions_elevation=ascensions_elevation,ascensions_labels=ascensions_labels)

@blueprint.route('/list')
@blueprint.route('/list.html')
@login_required
def list():
    pattern=request.args.get('pattern')
    #if pattern == '' :
    #    pattern="col"
    mode=request.args.get('mode')
    starred=request.args.get('starred')
    data = ga.retrieve_segments(pattern,mode,starred,session['uid'])
    ids = [row[1] for row in data]
    names = [row[0] for row in data]
    liststar = [row[2] for row in data]
    return render_template('home/list.html', segment='list',ids=ids, names=names,starred=liststar)



@blueprint.route('/userinfo')
@blueprint.route('/userinfo.html')
@login_required
def userinfo():
    user = ga.get_user(session['uid'])
    return render_template('home/userinfo.html', user=user)

@blueprint.route('/strava_auth_err')
@blueprint.route('/strava_auth_err.html')
@login_required
def stravaAuthErr():
    return render_template('home/strava_auth_err.html')

@blueprint.route('/synching')
@blueprint.route('/synching.html')
@login_required
def synching():
    la=0
    try: 
        la=int(ga.readLastActivity(session['uid']))
        print("Last Activity seen is ",la)
    except Exception as e:
        print("Can't get lastActivity",e)
    user = ga.get_user(session['uid'])
    url = "https://www.strava.com/api/v3/athlete/activities"

    p=1
    a=[]
    while p <= 1 : 
        r = requests.get(url + '?access_token=' + session['token']+"&per_page=100&page="+ str(p)+"&after=" + str(la))
        p=p+1
        r = r.json()
        print("Pat Add debug",r)
        if not r : 
            break
        if  isinstance(r, dict)  :
            if r['message'] == 'Rate Limit Exceeded':
                return render_template('home/strava_auth_err.html', user=user)
            if r['message'] == 'Authorization Error':
                refresh_token(session['uid'])
                return render_template('home/sync.html',message="votre jeton d'accès à strava a été renouvelé. Vous pouvez synchroniser vos activités")
        for s in  r :
            #if treatLast == True: 
            #    if s['id'] > la :
            #        a.append(str(s['id']))
            #else :
                if not ga.isActivityPresent(s['id']) :
                    a.append(str(s['id']))
    
    
    #a.reverse()
    for ac in a :
        print("Treat Activity=",ac)
        try : 
            ra=ga.addActivity(ac, session['token'])
            rs=ga.gse(ac,ra,session['token'])
            if rs == "quota exceeded":
                break
            ga.updateLastActivity(ra['start_date_local'],session['uid'])            
        except Exception as e:    
            print("An error was encountered with activity:", ac," ",e)
    return redirect(url_for('home_blueprint.dashboard'))

    #return render_template('/home/dashboard.html')

@blueprint.route('/sync')
@blueprint.route('/sync.html')
@login_required
def sync():
    message=request.args.get('message')
    return render_template('home/sync.html',segment='sync',message=message)

@blueprint.route('/heatmap')
@blueprint.route('/heatmap.html')
@login_required
def heatmap():
    activities = ga.get_ride_activities(session['uid'])
    activities_walk=ga.get_activities_by_type(session['uid'], "Type in (\"Run\",\"Walk\")" )
    return render_template('home/heatmap.html',segment='heatmap', activities=activities,activities_walk=activities_walk)

@blueprint.route('/activities')
@blueprint.route('/activities.html')
@login_required
def activities():
    limit=request.args.get('limit')
    if limit == None :
        limit==""
    offset=request.args.get('offset')
    if offset == None:
        offset=""
    count=len(ga.get_ride_activities(session['uid'])) 
    return render_template('home/activities.html',segment='activities',limit=limit,offset=offset,count=count)

@blueprint.route("/graph.html")
@blueprint.route("/graph")
def graph():
    sid=request.args.get('sid')
    name=request.args.get('name')
    datedeb=request.args.get('deb')
    datefin=request.args.get('fin')
    if datedeb == None:
        datedeb=""
    if datefin == None:
        datefin=""     
    #if pattern == '' :
    #    pattern="col"
    if sid == None :
        sid = "1234"

    data = ga.retrieve_segment_efforts(sid,session['uid'])
    labels = [row[1] for row in data]
    values = [row[0] for row in data]
    elevation=data[0][2]
    distance=data[0][3]
    elevation_rate=data[0][4]
    polyline=data[0][5]
    if polyline == None :
        polyline="}mzrGq~bb@Wi@Oq@GmA?}@?cADq@Lk@Ri@tB{EV}@XaB^uCVyCJgBNkFE_C_@qGQgBk@sDUmAcGyPSa@[gA_@_A_@s@OS"
    else:
        polyline=polyline.replace('\\', "\\\\")
    if elevation_rate < 0 :
        elevation=-elevation
    return render_template("home/graph.html", name=name,labels=labels,values=values,distance=distance,elevation=elevation,sid=sid,datedeb=datedeb,datefin=datefin,polyline=polyline)

@blueprint.route('/execute_command', methods=['POST'])
def execute_command():
    starred=request.args.get('starred')
    sid=request.args.get('sid')
    # Execute your Python code here based on the command
    ga.updateSegmentStarred(starred,sid,session['uid'])

    return "Command executed"+sid, 200


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
