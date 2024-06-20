from flask import Flask, request, jsonify
import requests
import json
import base64

gmaps_api_key = "AIzaSyATBUyS6xmGm6H4j5MxVWK--ZRO3Artcok"

weather_api_key = "e80884a1810f1d9a0e7e9cd5e6de93df"

app = Flask(__name__)


# GOOGLE DIRECTIONS
@app.route("/route", methods = ["POST"])
def get_route():
    base_url = "https://maps.googleapis.com/maps/api/directions/json"

    data = request.json
    start_coords = data["start coords"]
    end_coords = data["end coords"]

    params = {
        "origin": f"{start_coords[0]},{start_coords[1]}",
        "destination": f"{end_coords[0]},{end_coords[1]}",
        "mode": "walking",
        "key": gmaps_api_key,
    }

    trail_data = requests.get(base_url, params = params)
    trail_data = trail_data.json()
    
    if "routes" in trail_data and trail_data["routes"]:
        return trail_data
    else:
        error_message = data.get('error_message', 'Unknown error')
        return None, error_message


# GOOGLE ELEVATION
@app.route("/elevation", methods = ["POST"])    
def get_elevation():
    base_url = "https://maps.googleapis.com/maps/api/elevation/json"

    data = request.json

    encoded_polyline = data["route"]
    length = data["length"]

    params = {
        "path": f"enc:{encoded_polyline}",
        "samples": length//100,  # One sample every 100 meters
        "key": gmaps_api_key,
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



# GOOGLE STATICMAP
@app.route("/trailimage", methods = ["POST"])
def get_trail_image():
    data = request.json
    route = data["route"]
    
    base_url = "https://maps.googleapis.com/maps/api/staticmap"

    params = {
        "size": "600x400",
        "maptype": "hybrid",
        "path": f"color:0xff0000ff|weight:5|enc:{route}",  # Use the encoded polyline from the route
        "key": gmaps_api_key,
    }

    image_response = requests.get(base_url, params)


    if image_response.status_code == 200:
        image_data = base64.b64encode(image_response.content).decode("utf-8")
        return jsonify({
            "image_base64": image_data,
            })
    else:
        error_message = data.get('error_message', 'Unknown error')
        return None, error_message


# GOOGLE PLACES
@app.route('/searchhuts', methods=['POST'])
def search_huts():

    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    data = request.json
    coords = data["coordinates"]
    radius = data["radius"]
    params = {
        'key': gmaps_api_key,
        'location': coords,
        'radius': radius,
        'keyword': "mountain hut"
    }

    huts_data = requests.get(base_url, params=params)
    
    if huts_data.status_code == 200 and 'results' in huts_data.json():
        huts_data = huts_data.json()
        return jsonify(huts_data['results'])
    else:
        huts_data = huts_data.json()
        error_message = huts_data.get('error_message', 'Unknown error')
        return jsonify(None, error_message)

# GOOGLE GEOCODE
@app.route("/coordinates", methods = ["POST"])
def get_coordinates():
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    data = request.json
    location = data["location"]

    params = {
        "address": location,
        "key": gmaps_api_key
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data['status'] == 'OK':
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            return jsonify({'latitude': latitude, 'longitude': longitude}), 200
        else:
            return jsonify({'error': 'Geocoding was not successful'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# OPENWEATHERMAP
@app.route("/weatherforecast", methods=["POST"])
def get_weather_forecasts():
    base_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    try:
        data = request.json
        date = data["date"]
        lat = data["lat"]
        lon = data["lon"]

        complete_url = f"{base_url}?lat={lat}&lon={lon}&dt={date}&units=metric&appid={weather_api_key}"

        weather_response = requests.get(complete_url)
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            return jsonify(weather_data)
        else:
            return jsonify({"error": "Problem with your weather request"}), 404

    except KeyError:
        return jsonify({"error": "Invalid request data"}), 400

@app.route("/weathericon", methods = ["POST"])
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


    
if __name__ == "__main__":
    app.run(debug=True, port = 5050)
