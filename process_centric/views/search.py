from flask import Blueprint, request, redirect, url_for, session
import requests
from process_centric.consts import HUTS_URL

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/', methods=['POST', 'GET'])
def search():
    if 'google_id' not in session:
        return redirect(url_for('login.login', next=url_for('search.search')))
    data = request.get_json()
    location = data.get('location')
    radius = data.get('radius')

    results = requests.post(HUTS_URL, json = {
        'location': location,
        'radius': radius
    })

    return redirect(url_for('results.results', data=results))