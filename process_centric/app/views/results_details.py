import matplotlib.pyplot as plt
import io
import base64
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
import requests

import logging
from datetime import datetime
from process_centric.app.consts import GMAPS_API_KEY, TRAILS_URL, GEAR_URL, GET_FAVOURITE_GEAR_URL

results_details_blueprint = Blueprint('details', __name__)

import requests

def is_image_valid(image_url):
    try:
        response = requests.head(image_url)
        return response.status_code == 302 or response.status_code == 200
    except requests.RequestException:
        return False

@results_details_blueprint.route('/', methods=["POST", "GET"])
def results_details():
    if 'google_id' not in session:
        logging.debug("No user in session, redirecting to login.")
        login_url = url_for('auth.login')
        return redirect(login_url)
    
    hut_id = request.args.get('hut_id')
    gender = request.args.get('gender')
    huts_results = session.get('huts_results')
    weather = session.get('weather_results')
    date = session.get('search_date')
    start_location = session.get('search_location')
    
    if gender == 'woman':
        gender = 'W'
    elif gender == 'man':
        gender = 'M'
    if gender == 'not_specified':
        gender = 'any'

    date_obj = datetime(*date)
    day = date_obj.day
    suffix = "th" if 4 <= day <= 20 or 24 <= day <= 30 else ["st", "nd", "rd"][day % 10 - 1]
    formatted_date = date_obj.strftime(f"%A, {day}{suffix} %B %Y")

    if huts_results is None:
        return redirect('search.html')

    hut_data = next((hut for hut in huts_results if hut['id'] == hut_id), None)
    if hut_data is None:
        return redirect(url_for('error.error', error_message=f'Hut data not found', previous_url=request.referrer))

    try:
        trail = requests.post(TRAILS_URL, json={
            'start location': start_location,
            'end location': hut_data['name']
        }).json()
    
        gear = requests.post(GEAR_URL, json={
            'length': trail.get('length'),
            'elevations': trail.get('elevations'),
            'temperature': weather.get('weather').get('temperature') if weather else None,
            'weather': weather.get('weather').get('main') if weather else None,
            'prec': weather.get('weather').get('prec') if weather else None,
            'gender': gender
        }).json()
        route = trail.get('route')
    
        elevations = trail.get('elevations', [])
        distance_km = [i * 0.1 for i in range(len(elevations))]  # x axis in kilometers

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(distance_km, elevations, linestyle='-', color='b')
        ax.set_xlabel('Distance (km)')
        ax.set_ylabel('Elevation (m)')
        ax.set_title('Elevation Profile')
        ax.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        image_base64 = f"data:image/png;base64,{image_base64}"

        email = session['email']
        
        favourite_gear_response = requests.get(f'{GET_FAVOURITE_GEAR_URL}/{email}')
        favourite_gear_ids = []

        if favourite_gear_response.status_code == 200:
            favourite_gear_response = favourite_gear_response.json()
            for item in favourite_gear_response:
                gear_id = item.get('gearid')
                favourite_gear_ids.append(gear_id)

    
        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&maxheight=600&photoreference={hut_data['photo']['photo_reference']}&key={GMAPS_API_KEY}"
        if not is_image_valid(photo_url):
            photo_url = '/static/images/placeholder.png'

        map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=1920x1080&maptype=hybrid&path=color%3A0xff0000ff%7Cweight%3A5%7Cenc%3A{route}&key={GMAPS_API_KEY}"
        if not is_image_valid(map_url):
            map_url = '/static/images/placeholder.png'

        elevation_plot_url = image_base64  # This is already base64 encoded
        if not image_base64.startswith('data:image/png;base64,'):
            elevation_plot_url = '/static/images/placeholder.png'

    except Exception as e:
        message = ''
        """
        if str(e) == None or e == None:
            message = 'Unknown error'
        else:
            message = str(e)
        """
        return redirect(url_for('error.error', error_message='Encoutered error while computing the trail', previous_url=request.referrer))

        

    

    return render_template(
        'results_details.html',
        hut_data=hut_data,
        trail=trail,
        weather=weather,
        gear=gear,
        date=formatted_date,
        start_location=start_location,
        key=GMAPS_API_KEY,
        photo_url=photo_url,
        map_url=map_url,
        elevation_plot_url=elevation_plot_url,
        favourites=favourite_gear_ids,
        route=route
    )
