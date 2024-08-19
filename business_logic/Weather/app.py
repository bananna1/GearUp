from flask import Flask, request, jsonify
import requests
import json
import datetime
import logging
from consts import COORDS_URL, WEATHER_URL, WEATHER_ICON_URL

app = Flask(__name__)


@app.route("/weather", methods = ["POST"])
def get_weather():
    data = request.json
    date = data["date"]
    location = data["location"]

    coords = requests.post(COORDS_URL, json = {
            "location": location,
    })
    coords = coords.json()

    lat = coords["latitude"]
    lon = coords["longitude"]
    
    date_time = datetime.datetime(date[0], date[1], date[2], date[3], date[4], date[5])
    
    time_unix = int(date_time.timestamp())

    weather_forecasts = requests.post(WEATHER_URL, json = {
        "lat": lat,
        "lon": lon,
        "date": time_unix
    })

    weather_forecasts = weather_forecasts.json()

    main = weather_forecasts['data'][0]['weather'][0]['main']
    temperature = weather_forecasts['data'][0]['temp']
    prec = 0

    if main == 'Rain':
        prec = weather_forecasts['data'][0]['rain']['1h']

    weather = {
        'main': main,
        'temperature': temperature,
        'prec': prec
    }

    icon_code = weather_forecasts["data"][0]["weather"][0]["icon"]

    """
    weather_icon = requests.post(WEATHER_ICON_URL, json = {
        "icon id": icon_code
    })
    weather_icon = weather_icon.json()["image_base64"]
    """
    
    return jsonify({
        "weather": weather,
        "icon_id": icon_code
    })


if __name__ == "__main__":
    app.run(debug=True, port = 5001)