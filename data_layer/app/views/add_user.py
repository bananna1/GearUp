from flask import Blueprint, request, jsonify

from data_layer.app.models import Users

from data_layer.app import app
from data_layer.app import db

# Create a blueprint
add_user_blueprint = Blueprint('add_user', __name__)

def add_user(email, name, lastname):
        user = Users(email=email, name=name, lastname=lastname)
        db.session.add(user)
        db.session.commit()

@add_user_blueprint.route('/', methods=['POST'])
def add_user_endpoint():
    data = request.get_json()
    add_user(data['email'], data['name'], data['lastname'])
    return jsonify({'message': 'User added successfully'}), 201