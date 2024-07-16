from flask import Blueprint, request, jsonify
import requests
import base64
from adapter_layer.consts import GMAPS_API_KEY

# Create a blueprint
get_trail_image_blueprint = Blueprint('get_trail_image', __name__)

@get_trail_image_blueprint.route("/", methods=["POST"])
def get_trail_image():
    data = request.json
    route = data["route"]
    
    base_url = "https://maps.googleapis.com/maps/api/staticmap"

    params = {
        "size": "1920x1080",
        "maptype": "hybrid",
        "path": f"color:0xff0000ff|weight:5|enc:{route}",  # Use the encoded polyline from the route
        "key": GMAPS_API_KEY,
    }

    image_response = requests.get(base_url, params)


    if image_response.status_code == 200:
        print(image_response)
        image_data = base64.b64encode(image_response.content).decode("utf-8")
        return jsonify({
            "image_base64": image_data,
            })
    else:
        error_message = data.get('error_message', 'Unknown error')
        return None, error_message