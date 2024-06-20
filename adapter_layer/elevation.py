from flask import Blueprint, request, jsonify
import requests
from consts import GMAPS_API_KEY

# Create a blueprint
get_elevation_blueprint = Blueprint('get_elevation', __name__)

@get_elevation_blueprint.route("/", methods=["POST"])
def get_elevation():
    base_url = "https://maps.googleapis.com/maps/api/elevation/json"

    data = request.json

    encoded_polyline = data["route"]
    length = data["length"]

    params = {
        "path": f"enc:{encoded_polyline}",
        "samples": length//100,  # One sample every 100 meters
        "key": GMAPS_API_KEY,
    }

    elevation_data = requests.get(base_url, params=params)
    elevation_data = elevation_data.json()

    if "results" in elevation_data:
        elevations = [result["elevation"] for result in elevation_data["results"]]
        return jsonify({
            "elevations": elevations
            })
    else:
        error_message = elevation_data.get('error_message', 'Unknown error')
        return None, error_message