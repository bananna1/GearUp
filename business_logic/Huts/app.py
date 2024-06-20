from flask import Flask, request, jsonify
import requests
import json
from consts import COORDS_URL, HUTS_URL

app = Flask(__name__)

@app.route("/huts", methods = ["POST"])
def get_huts():
    data = request.json
    location = data.get('location')
    radius = data.get('radius', 10000)

    coords = requests.post(COORDS_URL, json = {
        "location": location
    })
    coords = coords.json()
    #print("COORDINATES", coords)
    lat = coords["latitude"]
    long = coords["longitude"]
    coords_str = str(lat) + ", " + str(long)

    huts_data = requests.post(HUTS_URL, json = {
        "coordinates": coords_str,
        "radius": radius
    })
    huts_data = huts_data.json()

    return jsonify(huts_data)


if __name__ == "__main__":
    app.run(debug=True, port=5003)

