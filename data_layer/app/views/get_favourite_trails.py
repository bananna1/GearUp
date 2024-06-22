from flask import Blueprint,jsonify

from data_layer.app.models import FavouriteTrails

# Create a blueprint
get_favourite_trails_blueprint = Blueprint('get_favourite_trails', __name__)

def get_favourite_gear(email):
    return FavouriteTrails.query.filter_by(email=email).all()

@get_favourite_trails_blueprint.route('/<string:email>', methods=['GET'])
def get_favourite_gear_endpoint(email):
    gear = get_favourite_gear(email)
    return jsonify(gear), 200
