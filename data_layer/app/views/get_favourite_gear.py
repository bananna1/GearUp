from flask import Blueprint,jsonify

from data_layer.app.models import FavouriteGear

# Create a blueprint
get_favourite_gear_blueprint = Blueprint('get_favourite_gear', __name__)

def get_favourite_gear(email):
    return FavouriteGear.query.filter_by(email=email).all()

@get_favourite_gear_blueprint.route('/<string:email>', methods=['GET'])
def get_favourite_gear_endpoint(email):
    gear = get_favourite_gear(email)
    if not gear:
        error_str = f'No favourite gear found for {email} in the database'
        return jsonify({'error': error_str}), 404
    return jsonify(gear), 200
