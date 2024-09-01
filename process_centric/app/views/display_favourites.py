from flask import redirect, url_for, session, Blueprint, render_template
import requests
from process_centric.app.consts import GET_FAVOURITE_GEAR_URL, GET_GEAR_URL
import logging

favourites_blueprint = Blueprint('favourites', __name__)

@favourites_blueprint.route('/', methods=['POST', 'GET'])
def favourites():
    if 'google_id' not in session:
        logging.debug("No user in session, redirecting to login.")
        login_url = url_for('auth.login')
        return redirect(login_url)
    
    email = session['email']
    
    favourite_gear_response = requests.get(f'{GET_FAVOURITE_GEAR_URL}/{email}')

    favourite_gear = []
    gear = []

    if favourite_gear_response.status_code == 200:
        #print('Favourite gear:', favourite_gear_response.json())
        favourite_gear = favourite_gear_response.json()
        for item in favourite_gear:
            gear_id = item.get('gearid')
            gear_item = requests.get(f'{GET_GEAR_URL}/{gear_id}').json()
            gear.append(gear_item)

    else:
        print('Failed to get favourite gear:', favourite_gear_response.status_code)
    
    

    
    return render_template('favourites.html', favourite_gear = gear)