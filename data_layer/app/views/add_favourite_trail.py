from flask import Blueprint, request, jsonify

from data_layer.app.models import FavouriteTrails
from data_layer.app import db

# Create a blueprint
add_favourite_trail_blueprint = Blueprint('add_favourite_trail', __name__)

def add_favourite_trail(email, gearid):
    favourite = FavouriteTrails(email=email, gearid=gearid)
    db.session.add(favourite)
    db.session.commit()

@add_favourite_trail_blueprint.route('/', methods=['POST'])
def add_favourite_trail_endpoint():
    data = request.get_json()
    add_favourite_trail(data['email'], data['gearid'])
    return jsonify({'message': 'Favourite gear inserted successfully'}), 201

