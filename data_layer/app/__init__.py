from flask import Flask, request, jsonify
from .db_operations import *
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

import os
from flask import Flask


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#db.init_app(app)
migrate = Migrate(app, db)

from data_layer.app.models import *
from data_layer.app.views.get_gear import get_gear_blueprint
from data_layer.app.views.add_favourite_gear import add_favourite_gear_blueprint
from data_layer.app.views.get_favourite_gear import get_favourite_gear_blueprint
from data_layer.app.views.add_favourite_trail import add_favourite_trail_blueprint
from data_layer.app.views.get_favourite_trails import get_favourite_trails_blueprint
from data_layer.app.views.add_user import add_user_blueprint


app.register_blueprint(get_gear_blueprint, url_prefix='/get_gear')
app.register_blueprint(add_favourite_gear_blueprint, urlprefix='/add_favourite_gear')
app.register_blueprint(get_favourite_gear_blueprint, urlprefix='/get_favourite_gear')
app.register_blueprint(add_favourite_trail_blueprint, urlprefix='/add_favourite_trail')
app.register_blueprint(get_favourite_trails_blueprint, urlprefix='/get_favourite_trails')
app.register_blueprint(add_user_blueprint, urlprefix='/add_user')

"""
def add_user(email, name, lastname):
    user = Users(email=email, name=name, lastname=lastname)
    db.session.add(user)
    db.session.commit()

def get_user_by_email(email):
    return FavouriteGear.query.filter_by(email=email).all()




@app.route('/get_favourites/<string:email>', methods=['GET'])
def get_favourites_endpoint(email):
    favourites = get_favourites(email)
    return jsonify(favourites), 200

"""