from flask import Flask, render_template, request, Response, jsonify, redirect, session
#from flask_cors import CORS

#from flask import Flask, render_template, request 
import ga
import json
import requests
import os
import urllib.parse
import requests

app = Flask(__name__)
CORS(app)

STRAVA_CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')


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


@app.route("/strava_token")
def strava_token():
    code = request.args.get('code')
    if not code:
        return Response('Error: Missing code param', status=400)
    return exchange_token(code)

@app.route("/")
def home():
    return render_template("dashboard.html")    

@app.route("/detailed")
def detailed():
    return render_template("detailed.html")    

@app.route("/segment/")
def segment():
    sid=request.args.get('sid')
    name="'"+request.args.get('name')+"'"
    datedeb=request.args.get('deb')
    datefin=request.args.get('fin')
    if datedeb == None:
        datedeb=""
    if datefin == None:
        datefin=""           
    
    data = ga.retrieve_segment_efforts(sid,session['uid'])
    labels = [row[1] for row in data]
    values = [row[0] for row in data]
   
    return render_template("graph.html", name=name,labels=labels, values=values,datedeb=datedeb,datefin=datefin)

@app.route("/segment_info/")
def segment_info():
    print("Pat Add", request)
    sid=request.args.get('sid')
    name="'"+request.args.get('name')+"'"
    data = ga.retrieve_segment_efforts(sid,session['uid'])
    labels = [row[1] for row in data]
    values = [row[0] for row in data]
    elevation = data[0][2]
    distance = data[0][3]

    #labels = ["January","February","March","April","May","June","July","August"]
    #values = [10,9,8,7,6,4,7,8]

    return render_template("segment_info.html",sid=sid,name=name,labels=labels, values=values, elevation=elevation, distance=distance)

@app.route("/graph.html")
def graph():
    return render_template("graph.html", name="''",labels=[], values=[])


@app.route('/list/')
def list():
    pattern=request.args.get('pattern')
    #if pattern == '' :
    #    pattern="col"
    mode=request.args.get('mode')
    starred=request.args.get('starred')
    print("Pat Add pattern='"+pattern+"' mode="+mode+"' starred="+str(starred))

    data = ga.retrieve_segments(pattern,mode,starred,session['uid'])
    ids = [row[1] for row in data]
    names = [row[0] for row in data]
    return render_template('list.html', names=json.dumps(names), ids=ids,starred=starred, pattern=pattern)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
