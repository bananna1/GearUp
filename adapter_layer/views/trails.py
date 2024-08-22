from flask import Blueprint, request, jsonify
import requests

from adapter_layer.consts import GMAPS_API_KEY

# Create a blueprint
get_trails_blueprint = Blueprint('get_trails', __name__)

@get_trails_blueprint.route("/", methods=["POST"])
def get_route():
    base_url = "https://maps.googleapis.com/maps/api/directions/json"

    try:
        data = request.json
        start_coords = data["start coords"]
        end_coords = data["end coords"]

        params = {
            "origin": f"{start_coords[0]},{start_coords[1]}",
            "destination": f"{end_coords[0]},{end_coords[1]}",
            "mode": "walking",
            "key": GMAPS_API_KEY,
        }
        trail_data = requests.get(base_url, params = params)
        trail_data = trail_data.json()
        
        if "routes" in trail_data and trail_data["routes"]:
            return trail_data
        else:
            error_message = data.get('error_message', 'Unknown error')
            return jsonify({"error": error_message}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500