from flask import Flask
from flask_session import Session
import redis

from process_centric.consts import *

from process_centric.views.auth import auth_blueprint
from process_centric.views.results_details import results_details_blueprint
from process_centric.views.search import search_blueprint
from process_centric.views.home import home_blueprint
from process_centric.views.display_favourites import favourites_blueprint
from process_centric.views.manage_favourites import manage_favourite_blueprint
from process_centric.views.error import error_blueprint

app = Flask(__name__)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(results_details_blueprint, url_prefix='/details')
app.register_blueprint(search_blueprint, url_prefix='/search')
app.register_blueprint(home_blueprint)
app.register_blueprint(favourites_blueprint, url_prefix='/favourites')
app.register_blueprint(manage_favourite_blueprint, url_prefix='/manage_favourite')
app.register_blueprint(error_blueprint, url_prefix='/error')


app.secret_key = b'8\xa1\x84\xe9\xf7\x93(o\xac9G\xe1\xe0h\xc8\x86\x14\xc0\xe9\xfeG\xbf\xca\xe0'

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.Redis(host='redis', port=6379)


Session(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)