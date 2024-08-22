from flask import Blueprint,jsonify

from data_layer.app.models import FavouriteGear


get_favourite_gear_blueprint = Blueprint('get_favourite_gear', __name__)


@get_favourite_gear_blueprint.route('/<string:email>', methods=['GET'])
def get_favourite_gear_endpoint(email):
    gear = FavouriteGear.query.filter_by(email=email).all()
    if not gear:
        error_str = f'No favourite gear found for {email} in the database'
        return jsonify({'error': error_str}), 404
    serialized_gear = [item.to_json() for item in gear]
    return jsonify(serialized_gear), 200
