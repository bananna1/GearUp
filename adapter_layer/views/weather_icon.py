from flask import Blueprint, request, jsonify
import requests
import base64
from adapter_layer.consts import WEATHER_API_KEY

# Create a blueprint
get_weather_icon_blueprint = Blueprint('get_weather_icon', __name__)

@get_weather_icon_blueprint.route("/", methods=["POST"])
def get_icon():
    base_icon_url = f"https://openweathermap.org/img/wn/"

    data = request.json

    icon_id = data["icon id"]

    complete_icon_url = f"{base_icon_url}{icon_id}@2x.png"

    icon_response = requests.get(complete_icon_url)

    if icon_response.status_code == 200:
        image_data = base64.b64encode(icon_response.content).decode("utf-8")
        return jsonify({"image_base64": image_data})
    else:
        return jsonify({"error": "problem fetching image"}), 404