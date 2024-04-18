# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json
import os
from flask import jsonify, render_template, redirect, request, url_for, session
from flask_login import (
    current_user,
    login_user,
    logout_user
)

import ga

from urllib.parse import urlsplit
from urllib.parse import parse_qs
import requests

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass


STRAVA_CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

def refresh_token(uid):
    user=ga.get_user(uid)
    print("Pat Add user=",user,uid)
    response = requests.post(
    url = 'https://www.strava.com/oauth/token',
    data = {
            'client_id': STRAVA_CLIENT_ID,
            'client_secret': STRAVA_CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': user[3]
            }
    )
    print("Pat Add debug strava request (in refresh _tokent)")
    # Save response as json in new variable
    new_strava_tokens = response.json()
    session['token']=new_strava_tokens['access_token']

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

# Login & Registration

@blueprint.route('/remove', methods=['GET', 'POST'])
def remove():
    current_user.remove()
    db.session.commit()
    return redirect(url_for('.login'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):
            login_user(user)
            print("Pat Add user=", user.id)
            session['uid']=user.id
            if user != None :
               refresh_token(user.id)

            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if 'code' in request.url: 
        parsed_url = urlsplit(request.url)
        raw_query_parameters = parsed_url.query
        query_parameters = parse_qs(raw_query_parameters)
        
        code=query_parameters['code'][0]

        strava_request = requests.post(
            'https://www.strava.com/oauth/token',
            data={
                'client_id': STRAVA_CLIENT_ID,
                'client_secret': STRAVA_CLIENT_SECRET,
                'code': code,
                'grant_type': 'authorization_code'
            }
        )
        print("Pat Add debug strava request (in login)")

        # si on a depasser le quota on renvoit vers l'authent ou vers le dashboard 
        if strava_request.status_code == 429:          
            if not current_user.is_authenticated:
                print("Pat Add current_user is"+current_user)
                return render_template('accounts/login.html',
                                form=login_form)
            else: 
                return redirect(url_for('home_blueprint.dashboard'))
        
        token=strava_request.json()
        session['token']=str(token['access_token'])
        print("Pat Add token=",str(strava_request.url), " token=",str(token))
        url = "https://www.strava.com/api/v3//athlete/"
    
        print("Pat Add debug strava request (in login2)")
        get_user_info=requests.get(url + '?access_token=' + str(token['access_token']))
        if get_user_info.status_code == 129:
            return render_template('accounts/login.html',
                                   msg='echec de la requete strava (probablement un depassement de quota, reessayer dans un moment)',
                                   form=login_form)
        user=ga.get_user(get_user_info.json())
        if user != None :
            print("Pat Add user_info is =",user[0],user[1], user[2])
            session['uid']=user[0]
            ga.update_refresh_token(user[0],token['refresh_token'])
        else : 
            print ("Pat Add user_info is =",user, type(user))
        user_i = Users.query.filter_by(id=user[0]).first()
        print("Pat Add user is ",user_i,type(user_i))
        if user_i == None :     
            return redirect('/register?id=' + str( user[0]) + '&email=enter_your_strava_mail@mail.com'+'&username='+user[2])
        else :
            login_user(user_i)

        return redirect(url_for('authentication_blueprint.route_default'))

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.dashboard'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
   
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:
        username = request.form['username']
        email = request.form['email']
        id = request.form['id']
        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        print("Pat Add user alchemy=",user.password)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        if 'email' in request.url: 
            username = request.args.get('username')
            email = request.args.get('email')
            id = request.args.get('id')
            return render_template('accounts/register.html',
                                   email=email,
                                   username=username,
                                   id=id,
                                   form=create_account_form)

    return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login')) 

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
