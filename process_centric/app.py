from flask import Flask, render_template, request, jsonify, redirect
import json
import requests
from process_centric.consts import *

from process_centric.views.login import login_blueprint
from process_centric.views.results_details import results_details_blueprint
from process_centric.views.search import search_blueprint
from process_centric.views.home import home_blueprint
from process_centric.views.favourites import favourites_blueprint

app = Flask(__name__)

app.register_blueprint(login_blueprint, url_prefix='/auth')
app.register_blueprint(results_details_blueprint, url_prefix='/details')
app.register_blueprint(search_blueprint, url_prefix='/search')
app.register_blueprint(home_blueprint)
app.register_blueprint(favourites_blueprint, url_prefix='/favourites')


app.secret_key = b'8\xa1\x84\xe9\xf7\x93(o\xac9G\xe1\xe0h\xc8\x86\x14\xc0\xe9\xfeG\xbf\xca\xe0'



if __name__ == "__main__":
    app.run(debug=True, port=5000)