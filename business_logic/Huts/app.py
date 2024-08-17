from flask import Flask, request, jsonify
import requests
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
    final_data = []
    for hut in huts_data:
        data = {
            'name': hut.get('name'),
            'rating': hut.get('rating'),
            'coordinates': {
                'hut_latitude': hut.get('geometry').get('location').get('lat'),
                'hut_longitude': hut.get('geometry').get('location').get('lng'),
            },
            'photo': {
                'photo reference': hut.get('photos')[0].get('photo_reference'),
                'photo height': hut.get('photos')[0].get('height'),
                'photo width': hut.get('photos')[0].get('width')
                }, 
        }
        final_data.append(data)

    return jsonify(final_data)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
