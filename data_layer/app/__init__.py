from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

import os
from flask import Flask

from data_layer.config import *

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from data_layer.app.models import *
from data_layer.app.views.get_gear import get_gear_blueprint
from data_layer.app.views.add_favourite_gear import add_favourite_gear_blueprint
from data_layer.app.views.get_favourite_gear import get_favourite_gear_blueprint
from data_layer.app.views.add_favourite_trail import add_favourite_trail_blueprint
from data_layer.app.views.get_favourite_trails import get_favourite_trails_blueprint
from data_layer.app.views.add_user import add_user_blueprint
from data_layer.app.views.get_user import get_user_blueprint


app.register_blueprint(get_gear_blueprint, url_prefix='/get_gear')
app.register_blueprint(add_favourite_gear_blueprint, urlprefix='/add_favourite_gear')
app.register_blueprint(get_favourite_gear_blueprint, urlprefix='/get_favourite_gear')
app.register_blueprint(add_favourite_trail_blueprint, urlprefix='/add_favourite_trail')
app.register_blueprint(get_favourite_trails_blueprint, urlprefix='/get_favourite_trails')
app.register_blueprint(add_user_blueprint, urlprefix='/add_user')
app.register_blueprint(get_user_blueprint, urlprefix='/get_user')