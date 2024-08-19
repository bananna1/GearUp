from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
import requests
import json
import logging
from process_centric.consts import GMAPS_API_KEY, TRAILS_URL, GEAR_URL


results_details_blueprint = Blueprint('details', __name__)

@results_details_blueprint.route('/', methods=["POST", "GET"])
def results_details():
    hut_id = request.args.get('hut_id')

    huts_results = session.get('huts_results')
    weather = session.get('weather_results')
    date = session.get('search_date')
    start_location = session.get('search_location')


    hut_data = next((hut for hut in huts_results if hut['id'] == hut_id), None)

    trail = requests.post(TRAILS_URL, json={
        'start location': start_location,
        'end location': hut_data['name']
    }).json()

    gear = requests.post(GEAR_URL, json={
        'length': trail.get('length'),
        'elevations': trail.get('elevations'),
        'temperature': weather.get('weather').get('temperature'),
        'weather': weather.get('weather').get('main'),
        'prec': weather.get('weather').get('prec')
    }).json()

    return render_template(
        'results_details.html',
        hut_data=hut_data,
        trail=trail,
        weather=weather,
        gear=gear,
        date=date,
        start_location=start_location,
        key=GMAPS_API_KEY
    )

    

