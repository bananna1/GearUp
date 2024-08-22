from flask import Flask, request, jsonify
import requests
import logging
from consts import COORDS_URL, HUTS_URL, HUT_IMAGE_URL

app = Flask(__name__)

@app.route("/huts", methods=["POST"])
def get_huts():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input. JSON data is required."}), 400
        
        location = data.get('location')
        if not location:
            return jsonify({"error": "Missing required parameter: 'location'"}), 400

        radius = data.get('radius', 10000)

        # Request coordinates for the provided location
        coords_response = requests.post(COORDS_URL, json={"location": location})
        if coords_response.status_code != 200:
            return jsonify({"error": "Failed to retrieve coordinates."}), coords_response.status_code
        
        try:
            coords = coords_response.json()
            lat = coords["latitude"]
            long = coords["longitude"]
        except (KeyError, ValueError) as e:
            return jsonify({"error": "Invalid response format from coordinates service."}), 500

        coords_str = f"{lat}, {long}"

        # Request huts within the given radius
        huts_response = requests.post(HUTS_URL, json={"coordinates": coords_str, "radius": radius})
        if huts_response.status_code != 200:
            return jsonify({"error": "Failed to retrieve huts data."}), huts_response.status_code

        try:
            huts_data = huts_response.json()
        except ValueError:
            return jsonify({"error": "Invalid response format from huts service."}), 500

        final_data = []
        for hut in huts_data:
            try:
                photo = hut.get('photos', [None])[0]
                if not photo:
                    continue  # Skip huts with no photo available

                photo_reference = photo.get('photo_reference')
                photo_height = photo.get('height')
                photo_width = photo.get('width')

                data = {
                    'id': hut.get('place_id'),
                    'name': hut.get('name'),
                    'rating': hut.get('rating'),
                    'coordinates': {
                        'hut_latitude': hut.get('geometry').get('location').get('lat'),
                        'hut_longitude': hut.get('geometry').get('location').get('lng'),
                    },
                    'photo': {
                        'photo_reference': photo_reference,
                        'photo_height': photo_height,
                        'photo_width': photo_width,
                    },
                }
                final_data.append(data)
            except (KeyError, IndexError) as e:
                logging.error(f"Failed to process hut data: {str(e)}")
                continue  # Skip this hut and move to the next

        return jsonify(final_data)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5003)
