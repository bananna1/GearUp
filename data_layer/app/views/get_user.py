from flask import Blueprint,jsonify

from data_layer.app.models import Users

# Create a blueprint
get_user_blueprint = Blueprint('get_user', __name__)

def get_user(email):
    return Users.query.filter_by(email=email).all()

@get_user_blueprint.route('/<string:email>', methods=['GET'])
def get_favourite_gear_endpoint(email):
    user = get_user(email)
    if not user:
        return jsonify({'error': 'User not found in the database'}), 404
    
    return jsonify(user), 200