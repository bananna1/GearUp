from flask import Blueprint, request, jsonify

from data_layer.app.models import FavouriteGear
from data_layer.app import db

# Create a blueprint
add_favourite_gear_blueprint = Blueprint('add_favourite_gear', __name__)

def add_favourite_gear(email, gearid):
    favourite = FavouriteGear(email=email, gearid=gearid)
    db.session.add(favourite)
    db.session.commit()

@add_favourite_gear_blueprint.route('/', methods=['POST'])
def add_favourite_gear_endpoint():
    data = request.get_json()
    add_favourite_gear(data['email'], data['gearid'])
    return jsonify({'message': 'Favourite gear inserted successfully'}), 201

