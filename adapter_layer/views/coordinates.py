from flask import Blueprint, request, jsonify
import requests
from adapter_layer.consts import GMAPS_API_KEY

get_coordinates_blueprint = Blueprint('get_coordinates', __name__)

@get_coordinates_blueprint.route("/", methods=["POST"])
def get_coordinates():
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    try:
        data = request.json
        location = data["location"]

        params = {
            "address": location,
            "key": GMAPS_API_KEY
        }
        
        response = requests.get(base_url, params=params)
        data = response.json()

        if data['status'] == 'OK':
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            return jsonify({'latitude': latitude, 'longitude': longitude}), 200
        else:
            return jsonify({'error': 'Geocoding was not successful'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500