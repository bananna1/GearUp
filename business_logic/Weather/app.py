from flask import Flask, request, jsonify
import requests
import json
import datetime
import logging
from consts import COORDS_URL, WEATHER_URL

app = Flask(__name__)

@app.route("/weather", methods=["POST"])
def get_weather():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input. JSON data is required."}), 400

        date = data.get("date")
        location = data.get("location")

        if not date or not location:
            return jsonify({"error": "Missing required parameters: 'date' and/or 'location'"}), 400

        if len(date) != 6:
            return jsonify({"error": "Date must be in the format [YYYY, MM, DD, HH, MM, SS]"}), 400

        # Get coordinates for the provided location
        coords_response = requests.post(COORDS_URL, json={"location": location})
        if coords_response.status_code != 200:
            return jsonify({"error": "Failed to retrieve coordinates."}), coords_response.status_code
        
        try:
            coords = coords_response.json()
            lat = coords["latitude"]
            lon = coords["longitude"]
        except (KeyError, ValueError) as e:
            return jsonify({"error": "Invalid response format from coordinates service."}), 500

        # Convert the date to Unix timestamp
        try:
            date_time = datetime.datetime(date[0], date[1], date[2], date[3], date[4], date[5])
            time_unix = int(date_time.timestamp())
        except (ValueError, TypeError) as e:
            return jsonify({"error": "Invalid date format."}), 400

        # Get weather data for the location and date
        weather_response = requests.post(WEATHER_URL, json={"lat": lat, "lon": lon, "date": time_unix})
        if weather_response.status_code != 200:
            return jsonify({"error": "Failed to retrieve weather data."}), weather_response.status_code
        
        try:
            weather_forecasts = weather_response.json()
            main = weather_forecasts['data'][0]['weather'][0]['main']
            temperature = weather_forecasts['data'][0]['temp']
            prec = 0

            if main == 'Rain':
                prec = weather_forecasts['data'][0].get('rain', {}).get('1h', 0)

            weather = {
                'main': main,
                'temperature': temperature,
                'prec': prec
            }

            icon_code = weather_forecasts["data"][0]["weather"][0]["icon"]

        except (KeyError, IndexError, ValueError) as e:
            return jsonify({"error": "Invalid response format from weather service."}), 500

        return jsonify({
            "weather": weather,
            "icon_id": icon_code
        })

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
