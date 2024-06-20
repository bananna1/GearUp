from flask import Flask, request, jsonify
import requests
import datetime
import json
import base64

base_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"

base_icon_url = f"https://openweathermap.org/img/wn/"

api_key = "e80884a1810f1d9a0e7e9cd5e6de93df"

app = Flask(__name__)

@app.route("/weather", methods=["POST"])
def get_weather_forecasts():
    try:
        data = request.json
        date = data["date"]
        lat = data["latitude"]
        lon = data["longitude"]

        date_time = datetime.datetime(date[0], date[1], date[2], date[3], date[4], date[5])

        print("date_time: ", date_time)

        # print Unix timestamp
        time_unix = int(date_time.timestamp())
        print("unix_timestamp ", time_unix)

        complete_url = f"{base_url}?lat={lat}&lon={lon}&dt={time_unix}&units=metric&appid={api_key}"
        print(complete_url)

        weather_response = requests.get(complete_url)

        if weather_response.status_code != 200:
            return jsonify({"error": "Problem with your weather request"}), 404

        weather_data = weather_response.json()

        print(json.dumps(weather_data, indent=4))  
        
        icon_code = weather_data["data"][0]["weather"][0]["icon"]

        icon_data = get_icon(icon_code)["image_base64"]

        return jsonify({
            "weather data": weather_data,
            "weather icon": icon_data,
        })

    except KeyError:
        return jsonify({"error": "Invalid request data"}), 400

def get_icon(icon_id):
    complete_icon_url = f"{base_icon_url}{icon_id}@2x.png"

    icon_response = requests.get(complete_icon_url)

    if icon_response.status_code == 200:
        image_data = base64.b64encode(icon_response.content).decode("utf-8")
        return {"image_base64": image_data}
    else:
        return jsonify({"error": "problem fetching image"}), 404


"""
request_structure = {
    date, # list of integers representing the date
    latitude, # latitude of the place
    longitude, # longitude of the place
}
"""

if __name__ == "__main__":
    app.run(debug=True)