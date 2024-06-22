from flask import Blueprint, request, jsonify
import requests
from adapter_layer.consts import GMAPS_API_KEY

# Create a blueprint
get_huts_blueprint = Blueprint('get_huts', __name__)

@get_huts_blueprint.route("/", methods=["POST"])
def search_huts():

    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    data = request.json
    coords = data["coordinates"]
    radius = data["radius"]
    params = {
        'key': GMAPS_API_KEY,
        'location': coords,
        'radius': radius,
        'keyword': "mountain hut"
    }

    huts_data = requests.get(base_url, params=params)
    
    if huts_data.status_code == 200 and 'results' in huts_data.json():
        huts_data = huts_data.json()
        return jsonify(huts_data['results'])
    else:
        huts_data = huts_data.json()
        error_message = huts_data.get('error_message', 'Unknown error')
        return jsonify(None, error_message)