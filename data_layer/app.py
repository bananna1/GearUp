from flask import Flask, request, jsonify
from db_operations import insert_gear, get_gear, insert_favourite, get_favourites
from flask_sqlalchemy import SQLAlchemy
from config import basedir, SECRET_KEY, SQLALCHEMY_DATABASE_URI,  SQLALCHEMY_TRACK_MODIFICATIONS
from flask_migrate import Migrate  # Import Migrate
#from .seed_data import seed_db_command  # Import CLI commands
#from . import db_commands 

app = Flask(__name__)

db = SQLAlchemy()

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/insert_gear', methods=['POST'])
def insert_gear_endpoint():
    data = request.get_json()
    insert_gear(data)
    return jsonify({'message': 'Gear inserted successfully'}), 201

@app.route('/get_gear/<int:code>', methods=['GET'])
def get_gear_endpoint(code):
    gear = get_gear(code)
    return jsonify(gear), 200

@app.route('/insert_favourite', methods=['POST'])
def insert_favourite():
    data = request.get_json()
    insert_favourite(data['email'], data['gearid'])
    return jsonify({'message': 'Favourite gear inserted successfully'}), 201

@app.route('/get_favourites/<string:email>', methods=['GET'])
def get_favourites_endpoint(email):
    favourites = get_favourites(email)
    return jsonify(favourites), 200

if __name__ == '__main__':
    app.run(debug=True, port=5051)
