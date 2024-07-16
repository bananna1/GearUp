from flask import Blueprint,jsonify

from data_layer.app.models import FavouriteTrails

# Create a blueprint
get_favourite_trails_blueprint = Blueprint('get_favourite_trails', __name__)

def get_favourite_trails(email):
    return FavouriteTrails.query.filter_by(email=email).all()

@get_favourite_trails_blueprint.route('/<string:email>', methods=['GET'])
def get_favourite_trails_endpoint(email):
    trails = get_favourite_trails(email)
    if not trails:
        error_str = f'No favourite trails found for {email} in the database'
        return jsonify({'error': error_str}), 404
    return jsonify(trails), 200
