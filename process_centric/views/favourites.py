from flask import redirect, url_for, session, Blueprint, render_template
import requests
from process_centric.consts import *
import logging

favourites_blueprint = Blueprint('favourites', __name__)

@favourites_blueprint.route('/', methods=['POST', 'GET'])
def favourites():
    if 'google_id' not in session:
        return redirect(url_for('login.login', next=url_for('favourites.favourites')))

    logging.debug('SONO QUI')
    email = session['email']
    
    favourite_gear_response = requests.get(f'{GET_FAVOURITE_GEAR_URL}/{email}')

    favourite_gear = []

    if favourite_gear_response.status_code == 200:
        print('Favourite gear:', favourite_gear_response.json())
        favourite_gear = favourite_gear_response.json()
    else:
        print('Failed to get favourite gear:', favourite_gear_response.status_code)
    
    favourite_trails_response = requests.get(f'{GET_FAVOURITE_TRAILS_URL}/{email}')
    favourite_trails = []

    if favourite_trails_response.status_code == 200:
        print('Favourite trails:', favourite_trails_response.json())
        favourite_trails = favourite_trails_response.json()
    else:
        print('Failed to get favourite trails:', favourite_trails_response.status_code)

    return render_template('favourites.html', favourite_gear = favourite_gear, favourite_trails = favourite_trails)