from flask import Blueprint, request, redirect, url_for, session, render_template, jsonify
import requests
import json
import logging
from process_centric.consts import HUTS_URL
from process_centric.consts import WEATHER_URL
import datetime
import urllib.parse
from process_centric.consts import GMAPS_API_KEY

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/')
def search_page():
    today = datetime.datetime.now().date()
    max_date = today + datetime.timedelta(days=5)
    return render_template('search.html', today=today, max_date=max_date)

@search_blueprint.route('/results', methods=['POST', 'GET'])
def search():
    if 'google_id' not in session:
        return redirect(url_for('login.login', next=url_for('search.search')))
    
    location = request.form.get('location')
    #print(location)
    radius = int(request.form.get('radius')) * 1000 # from kilometersto meters
    #print(radius)
    date = request.form.get('date')

    date = date.split("-")

    for i in range(len(date)):
        date[i] = int(date[i])


    date.append(10)
    date.append(0)
    date.append(0)

    logging.debug(date)

    huts_results = requests.post(HUTS_URL, json = {
        'location': location,
        'radius': radius
    })
    huts_results = huts_results.json()
    #print(huts_results)
    weather_results = requests.post(WEATHER_URL, json = {
        'date': date,
        'location': location
    })
    weather_results = weather_results.json()

    results = {
        'huts_results': huts_results,
        'weather_results': weather_results
    }

    session['huts_results'] = huts_results
    session['weather_results'] = weather_results
    session['search_date'] = date
    session['search_location'] = location


    today = datetime.datetime.now().date()
    max_date = today + datetime.timedelta(days=5)


    return render_template('search.html', today=today, max_date=max_date, results=results, key=GMAPS_API_KEY, location=location, chosen_date=date)
