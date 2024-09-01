from flask import Blueprint, request, redirect, url_for, session, render_template, jsonify
import requests
import json
import logging
from process_centric.app.consts import HUTS_URL
from process_centric.app.consts import WEATHER_URL
import datetime
import urllib.parse
from process_centric.app.consts import GMAPS_API_KEY

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/')
def search_page():
    if 'google_id' not in session:
        logging.debug("No user in session, redirecting to login.")
        login_url = url_for('auth.login')
        return redirect(login_url)

    today = datetime.datetime.now().date()
    max_date = today + datetime.timedelta(days=4)
    return render_template('search.html', today=today, max_date=max_date)

@search_blueprint.route('/results', methods=['POST', 'GET'])
def search():
    if 'google_id' not in session:
        logging.debug("No user in session, redirecting to login.")
        login_url = url_for('auth.login')
        return redirect(login_url)
    
    try:
        location = request.form.get('location')
        #print(location)
        radius = int(request.form.get('radius')) * 1000 # from kilometers to meters
        #print(radius)
        date = request.form.get('date')

        date = date.split("-")

        for i in range(len(date)):
            date[i] = int(date[i])


        date.append(10)
        date.append(0)
        date.append(0)

        #logging.debug(date)

        gender = request.form.get('gender')

        huts_results = requests.post(HUTS_URL, json = {
            'location': location,
            'radius': radius
        })
        if huts_results.status_code == 500:
            message = huts_results.json().get('error')
            return redirect(url_for('error.error', error_message=message, previous_url=request.referrer))

            
        huts_results = huts_results.json()
        #print(huts_results)
        weather_results = requests.post(WEATHER_URL, json = {
            'date': date,
            'location': location
        })
        if weather_results.status_code == 500:
            message = weather_results.json().get('error')
            return redirect(url_for('error.error', error_message=message, previous_url=request.referrer))

        weather_results = weather_results.json()
        

        results = {
            'huts_results': huts_results,
            'weather_results': weather_results
        }

        session['huts_results'] = huts_results
        session['weather_results'] = weather_results
        session['search_date'] = date
        session['search_location'] = location
        session['gender'] = gender

        today = datetime.datetime.now().date()
        max_date = today + datetime.timedelta(days=4)

    except Exception as e:
        results = {
            'huts_results': session['huts_results'],
            'weather_results': session['weather_results']
        }   
        location = session['search_location']
        date = session['search_date']
        gender = session['gender']
        #logging.debug(session)

        today = datetime.datetime.now().date()
        max_date = today + datetime.timedelta(days=4)



    return render_template('search.html', today=today, max_date=max_date, results=results, key=GMAPS_API_KEY, location=location, chosen_date=date, gender=gender)



    
    #logging.debug(session)

    today = datetime.datetime.now().date()
    max_date = today + datetime.timedelta(days=4)


    return render_template('search.html', today=today, max_date=max_date, results=results, key=GMAPS_API_KEY, location=location, chosen_date=date, gender=gender)
