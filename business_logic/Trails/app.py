from flask import Flask, request, jsonify
import requests
import json
from consts import COORDS_URL, ROUTE_URL, ELEVATION_URL, TRAILIMAGE_URL

app = Flask(__name__)

@app.route("/trails", methods=["POST"])
def trails_service():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid input. JSON data is required."}), 400

    start_location = data.get('start location')
    end_location = data.get('end location')

    if not start_location or not end_location:
        return jsonify({"error": "Both 'start location' and 'end location' are required."}), 400

    try:
        start_coords_response = requests.post(COORDS_URL, json={"location": start_location})
        start_coords_response.raise_for_status()
        start_coords = start_coords_response.json()

        end_coords_response = requests.post(COORDS_URL, json={"location": end_location})
        end_coords_response.raise_for_status()
        end_coords = end_coords_response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to retrieve coordinates: {str(e)}"}), 500

    try:
        start_lat = start_coords["latitude"]
        start_long = start_coords["longitude"]

        end_lat = end_coords["latitude"]
        end_long = end_coords["longitude"]
    except KeyError as e:
        return jsonify({"error": f"Missing coordinate data: {str(e)}"}), 500

    try:
        trail_data_response = requests.post(ROUTE_URL, json={
            "start coords": [start_lat, start_long],
            "end coords": [end_lat, end_long]
        })
        trail_data_response.raise_for_status()
        trail_data = trail_data_response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to retrieve trail data: {str(e)}"}), 500

    try:
        polyline = trail_data["routes"][0]["overview_polyline"]["points"]
        length = trail_data["routes"][0]["legs"][0]["distance"]["value"]
    except (KeyError, IndexError) as e:
        return jsonify({"error": f"Unexpected trail data format: {str(e)}"}), 500

    try:
        elevations_response = requests.post(ELEVATION_URL, json={
            "route": polyline,
            "length": length
        })
        elevations_response.raise_for_status()
        elevations_data = elevations_response.json()
        elevations = elevations_data["elevations"]
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to retrieve elevations data: {str(e)}"}), 500
    except json.decoder.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON from elevations endpoint"}), 500
    except KeyError as e:
        return jsonify({"error": f"Unexpected elevations data format: {str(e)}"}), 500

    link = f"https://www.google.com/maps/dir/{start_lat},{start_long}/{end_lat},{end_long}"

    return jsonify({
        "link": link,
        "length": length,
        "elevations": elevations,
        "route": polyline
        # "image data": image_data
    })


if __name__ == "__main__":
    app.run(debug=True, port=5002)
