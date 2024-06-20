from flask import Flask, request, jsonify
import requests
import json
from consts import COORDS_URL, ROUTE_URL, ELEVATION_URL, TRAILIMAGE_URL


app = Flask(__name__)


@app.route("/trails", methods = ["POST"])
def trails_service():
    data = request.json

    start_location = data.get('start location')
    end_location = data.get('end location')

    start_coords = requests.post(COORDS_URL, json = {
        "location": start_location
    })

    end_coords = requests.post(COORDS_URL, json = {
        "location": end_location
    })

    start_coords = start_coords.json()
    end_coords = end_coords.json()
    try:
        start_lat = start_coords["latitude"]
        start_long  = start_coords["longitude"]

        end_lat = end_coords["latitude"]
        end_long  = end_coords["longitude"] 
    
    except Exception as e:

        return jsonify({
            "error": start_coords["error"]
        })

    trail_data = requests.post(ROUTE_URL, json = {
        "start coords": [start_lat, start_long],
        "end coords": [end_lat, end_long]
    })

    trail_data = trail_data.json()

    # Extract the encoded polyline representing the route
    polyline = trail_data["routes"][0]["overview_polyline"]["points"]
    # Extract the length of the route
    length = trail_data["routes"][0]["legs"][0]["distance"]["value"]


    # Inside the trails_service function in APP 1
    elevations_response = requests.post(ELEVATION_URL, json={
        "route": polyline,
        "length": length
    })

    if elevations_response.status_code == 200:
        try:
            elevations_data = elevations_response.json()
            elevations = elevations_data["elevations"]
        except json.decoder.JSONDecodeError as e:
            return jsonify({"error": "Error decoding JSON from elevations endpoint"}), 500
    else:
        return jsonify({"error": "Failed to retrieve elevations data"}), elevations_response.status_code


    link = f"https://www.google.com/maps/dir/{start_lat},{start_long}/{end_lat},{end_long}"

    image_data = requests.post(TRAILIMAGE_URL, json = {
        "route": polyline
    })
    image_data = image_data.json()

    return jsonify({
        "link": link, 
        "length": length,
        "elevations": elevations,   
        "image data": image_data
    })



if __name__ == "__main__":
    app.run(debug=True, port = 5002)