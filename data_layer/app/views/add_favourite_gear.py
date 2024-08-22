from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from data_layer.app.models import FavouriteGear
from data_layer.app import db

add_favourite_gear_blueprint = Blueprint('add_favourite_gear', __name__)

@add_favourite_gear_blueprint.route('/', methods=['POST'])
def add_favourite_gear_endpoint():
    data = request.get_json()
    email = data.get('email')
    gearid = data.get('gearid')  
   
    favourite = FavouriteGear(email=email, gearid=gearid)

    try:
        db.session.add(favourite)
        db.session.commit()
        return jsonify({'message': 'Favourite gear inserted successfully'}), 201
    except IntegrityError:

        db.session.rollback()
        return jsonify({'message': 'Favourite gear already exists'}), 400
