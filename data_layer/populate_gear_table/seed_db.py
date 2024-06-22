"""
import json
import sys 
import os
from flask_sqlalchemy import SQLAlchemy

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root directory to sys.path
sys.path.append(project_root)

from data_layer import app

from data_layer.app import db
from data_layer.app.models import Gear

def seed_db():
    with app.app_context():
        #Seed the database with initial data
        with open('gear_data.json') as f:
            gear_data = json.load(f)
            for item in gear_data:
                print(item)
                gear = Gear(
                    code=item['id'],
                    description=item['description'],
                    gender=item['gender'],
                    category=item['category'],
                    warmth=item['warmth'],
                    waterproof=item['waterproof'],
                    level=item['level'],
                    link=item['link']
                )
                db.session.add(gear)
            db.session.commit()
    print('Database seeded!')

def display_gear_table():
    gear_items = Gear.query.all()
    for item in gear_items:
        print(item)

seed_db()
display_gear_table()
"""