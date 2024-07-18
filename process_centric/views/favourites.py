from flask import redirect, url_for, session, request, flash, Blueprint
import requests
from process_centric.consts import *
favourites_blueprint = Blueprint('favourites', __name__)

@favourites_blueprint.route('/', methods=['POST'])
def favourites():
    if 'google_id' not in session: # CAPIRE COME PASSARE INFORMAZIONI SULLA SESSIONE
        return redirect(url_for('auth.login', next=url_for('favourites')))

    email = session['email']
    favourite_gear_response = requests.get(f'{GET_FAVOURITE_GEAR_URL}/{email}')

    if favourite_gear_response.status_code == 200:
        print('Favourite gear:', favourite_gear_response.json())
    else:
        print('Failed to get favourite gear:', favourite_gear_response.status_code)

    
    favourite_trails_response = requests.get(f'{GET_FAVOURITE_TRAILS_URL}/{email}')

    if favourite_trails_response.status_code == 200:
        print('Favourite trails:', favourite_trails_response.json())
    else:
        print('Failed to get favourite trails:', favourite_trails_response.status_code)

        