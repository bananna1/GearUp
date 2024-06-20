from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

api_key = "AIzaSyATBUyS6xmGm6H4j5MxVWK--ZRO3Artcok"

@app.route('/huts', methods=['POST'])
def search_huts():
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'No JSON data provided'}), 400

    location = request_data.get('location')
    radius = request_data.get('radius', 10000)

    huts = search_mountain_huts(location, radius)
    if huts:
        return jsonify(huts)
    else:
        return jsonify({'error': 'No huts found'})



def search_mountain_huts(location, radius=10000, keyword='mountain hut'):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'key': api_key,
        'location': location,
        'radius': radius,
        'keyword': keyword
    }

    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code == 200 and 'results' in data:
        return data['results']
    else:
        error_message = data.get('error_message', 'Unknown error')
        return None, error_message

if __name__ == '__main__':
    app.run(debug=True)
