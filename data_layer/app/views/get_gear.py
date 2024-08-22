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
    specs = request.json
    
    category = specs.get('category')
    warmth = specs.get('warmth')
    waterproof = specs.get('waterproof')
    level = specs.get('level')
    gender = specs.get('gender')

    filter_params = {
        'category': category,
        'warmth': warmth,
        'waterproof': waterproof,
        'level': level,
        'gender': gender
    }

    logging.debug(warmth, waterproof, level, gender)

    filtered_params = {key: value for key, value in filter_params.items() if value != 'any'}

    
    query = Gear.query

    for key, value in filtered_params.items():
        if key == 'waterproof':
            
            query = query.filter(Gear.waterproof >= value)
        else:
            
            query = query.filter(getattr(Gear, key) == value)

    
    gear = query.all()
    gear_list = [item.to_json() for item in gear]

    logging.debug(f"Gear found: {gear_list}")
    return jsonify(gear_list), 200
