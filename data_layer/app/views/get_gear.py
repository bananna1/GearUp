from flask import Blueprint, jsonify, request
import requests
import json
import logging
from data_layer.app.models import Gear

get_gear_blueprint = Blueprint('get_gear', __name__)
    

@get_gear_blueprint.route('/id/<int:code>', methods=['GET'])
def get_gear(code):
    gear = Gear.query.get(code).to_json()
    return jsonify(gear), 200

@get_gear_blueprint.route('/', methods = ['POST'])
def get_gear_specs():
    logging.debug('SONO QUIIIIIIIIIIIIIIIIIIIIIIIIIII')
    specs = request.json
    warmth = specs.get('warmth')
    waterproof = specs.get('waterproof')
    level = specs.get('level')
    gender = specs.get('gender')

    logging.debug(warmth, waterproof, level, gender)

    
    if gender != 'any':
        gear = Gear.query.filter_by(warmth=warmth, waterproof=waterproof, level=level, gender=gender)
    
    else:
        gear = Gear.query.filter_by(warmth=warmth, waterproof=waterproof, level=level)

    gear = [item.to_json() for item in gear.all()]

    logging.debug(f"Gear found: {gear}")
    return jsonify(gear), 200

