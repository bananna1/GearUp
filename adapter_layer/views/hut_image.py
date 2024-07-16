from flask import Blueprint, request, jsonify
import requests
import base64
from PIL import Image
from io import BytesIO
from adapter_layer.consts import GMAPS_API_KEY

# Create a blueprint
get_hut_image_blueprint = Blueprint('get_hut_image', __name__)

@get_hut_image_blueprint.route("/", methods=["POST"])
def get_hut_image():
    photo_reference = request.json
    max_width = 1920
    max_height = 1080
    url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&maxheight={max_height}&photoreference={photo_reference}&key={GMAPS_API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        image_data = base64.b64encode(response.content).decode('utf-8')

        return jsonify({
            "image_base64": image_data
        })
    else:
        error_message = photo_reference.get('error_message', 'Unknown error')
        return None, error_message