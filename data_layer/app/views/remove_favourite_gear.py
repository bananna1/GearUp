from flask import Blueprint, request, jsonify

from data_layer.app.models import FavouriteGear
from data_layer.app import db


remove_favourite_gear_blueprint = Blueprint('remove_favourite_gear', __name__)


@remove_favourite_gear_blueprint.route('/', methods=['POST'])
def remove_favourite_gear_endpoint():
    data = request.get_json()
    email = data['email']
    gear_id = data['gearid']
    
    favourite_gear = FavouriteGear.query.filter_by(email=email, gear_id=gear_id).first()

    if favourite_gear:
        
        db.session.delete(favourite_gear)
        db.session.commit()
        return jsonify({'message': 'Favourite gear removed successfully'}), 200
    else:
        return jsonify({'error': 'Favourite gear not found.'}), 404

