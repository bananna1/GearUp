from flask import Blueprint, request, jsonify
import requests
import base64
from adapter_layer.consts import GMAPS_API_KEY

# Create a blueprint
get_hut_image_blueprint = Blueprint('get_hut_image', __name__)

@get_hut_image_blueprint.route("/", methods=["POST"])
def get_hut_image():
    photo_data = request.json
    photo_reference = photo_data.get('photo reference')
    width = photo_data.get('width')
    height = photo_data.get('height')
    url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={width}&maxheight={height}&photoreference={photo_reference}&key={GMAPS_API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        image_data = base64.b64encode(response.content).decode('utf-8')

        return jsonify({ 
            "image_base64": image_data
        })
    else:
        error_message = photo_reference.get('error_message', 'Unknown error')
        return None, error_message