# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from signal import sigtimedwait
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import requests
import ga
import json

@blueprint.route('/index')
@login_required
def index():
    print("Patounet Add")

    return render_template('home/index.html', segment='index')

@blueprint.route('/ascensions')
@blueprint.route('/ascensions.html')
@login_required
def ascensions():
    print("Pat Add")
    pattern=request.args.get('pattern')
    if pattern == None :
        pattern=""
    mode=request.args.get('mode')
    if mode == None:
        mode="like"
    starred=request.args.get('starred')
    if starred == None:
        starred="false"
    print("Pat Add pattern='"+str(pattern)+"' mode="+str(mode))

    datasegments = ga.retrieve_segments(pattern,mode,starred)
    ids = [row[1] for row in datasegments]
    names = [row[0] for row in datasegments]
    print("Pat Add names=",len(names))

    data = ga.retrieve_segment_efforts("5855232")
    labels = [row[1] for row in data]
    values = [row[0] for row in data]
    return render_template('home/ascensions.html', segment='ascensions',datasegments=datasegments,ids=ids,names=names,labels=labels, values=values,pattern=pattern,mode=mode,starred=starred)

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
    if starred == None:
        starred="false"

    activities = ga.retrieve_activities()
    ascensions =  ga.retrieve_ascensions(5)
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
    return render_template('home/dashboard.html', segment='dashboard',distance=distance,moving_time=moving_time,elevation=elevation,average_speed=average_speed,max_speed=max_speed,average_cadence=average_cadence,average_temp=average_temp,gear_name=gear_name,gear_distance=gear_distance,activities_labels=activities_labels,ascensions_distance=ascensions_distance,ascensions_moving_time=ascensions_moving_time,ascensions_elevation=ascensions_elevation,ascensions_labels=ascensions_labels)

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

    activities = ga.retrieve_activities()
    ascensions =  ga.retrieve_ascensions(5)
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
    print("Pat Add pattern='"+pattern+"' mode="+mode+"' starred="+str(starred))

    data = ga.retrieve_segments(pattern,mode,starred)
    ids = [row[1] for row in data]
    names = [row[0] for row in data]
    return render_template('home/list.html', segment='list',ids=ids, names=names)




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
    print("Pat Add sid=",sid)
    if sid == None :
        sid = "1234"

    data = ga.retrieve_segment_efforts(sid)
    labels = [row[1] for row in data]
    values = [row[0] for row in data]
    elevation=data[0][2]
    distance=data[0][3]
    elevation_rate=data[0][4]
    if elevation_rate < 0 :
        elevation=-elevation
    return render_template("home/graph.html", name=name,labels=labels,values=values,distance=distance,elevation=elevation,sid=sid,datedeb=datedeb,datefin=datefin)


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
