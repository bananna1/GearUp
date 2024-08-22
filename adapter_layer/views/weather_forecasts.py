from flask import Blueprint, request, jsonify
import requests
from adapter_layer.consts import WEATHER_API_KEY

# Create a blueprint
get_weather_forecasts_blueprint = Blueprint('get_weather_forecasts', __name__)

@get_weather_forecasts_blueprint.route("/", methods=["POST"])
def get_weather_forecasts():
    base_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    try:
        data = request.json
        date = data["date"]
        lat = data["lat"]
        lon = data["lon"]

        complete_url = f"{base_url}?lat={lat}&lon={lon}&dt={date}&units=metric&appid={WEATHER_API_KEY}"

        weather_response = requests.get(complete_url)
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            return jsonify(weather_data)
        else:
            return jsonify({"error": "Problem with your weather request"}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500