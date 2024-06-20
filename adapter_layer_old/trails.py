from flask import Flask, request, jsonify
import requests
import json
import base64

api_key = "AIzaSyATBUyS6xmGm6H4j5MxVWK--ZRO3Artcok"

app = Flask(__name__)

@app.route("/trail", methods = ["POST"])
def get_trail():
    
    data = request.json
    start_coords = data["start_coords"]
    end_coords = data["end_coords"]

    # Retrieve route using Directions API
    route, length = get_route(start_coords, end_coords)
    # Retrieve elevation data using Elevation API
    elevation = get_elevation(route, length)
    print("Elevation:", elevation)

    # Generate the static map image
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "size": "600x400",
        "maptype": "hybrid",
        "path": f"color:0xff0000ff|weight:5|enc:{route}",  # Use the encoded polyline from the route
        "key": api_key,
    }

    image_response = requests.get(base_url, params=params)

    if image_response.status_code == 200:
        image_data = base64.b64encode(image_response.content).decode("utf-8")
        return jsonify({
            "length": length,
            "elevation": elevation,
            "image_base64": image_data,
            })
    else:
        print("Error fetching map image. Check your API key and parameters.")



def get_route(start_coords, end_coords):

    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{start_coords[0]},{start_coords[1]}",
        "destination": f"{end_coords[0]},{end_coords[1]}",
        "mode": "walking",
        "key": api_key,
    }

    response = requests.get(base_url, params = params)
    trail_data = response.json()
    print("DATA \n \n", json.dumps(trail_data, indent = 4), "\n \n")
    length = trail_data["routes"][0]["legs"][0]["distance"]["value"]
    print ("LENGTH", length)

    if "routes" in trail_data and trail_data["routes"]:
        # Extract the encoded polyline representing the route
        encoded_polyline = trail_data["routes"][0]["overview_polyline"]["points"]
        return encoded_polyline, length
    else:
        print("Error fetching route. Check your API key and parameters.")
        return None
    
def get_elevation(encoded_polyline, length):
    base_url = "https://maps.googleapis.com/maps/api/elevation/json"
    params = {
        "path": f"enc:{encoded_polyline}",
        "samples": length//100,  # One sample every 100 meters
        "key": api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "results" in data:
        elevations = [result["elevation"] for result in data["results"]]
        return elevations
    else:
        print("Error fetching elevation data. Check your API key and parameters.")
        return None
    
if __name__ == "__main__":
    app.run(debug=True, port = 5050)
