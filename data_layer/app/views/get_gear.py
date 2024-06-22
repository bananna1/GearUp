from flask import Blueprint, jsonify

from data_layer.app.models import Gear

# Create a blueprint
get_gear_blueprint = Blueprint('get_gear', __name__)

def get_gear(code):
    return Gear.query.get(code)

@get_gear_blueprint.route('/<int:code>', methods=['GET'])
def get_gear_endpoint(code):
    gear = get_gear(code)
    return jsonify(gear), 200
