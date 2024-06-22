"""
import sys
import os
from data_layer.app import db
from data_layer.app.models import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def insert_gear(data):
    gear = Gear(
        code=data['code'],
        description=data['description'],
        gender=data['gender'],
        category=data['category'],
        warmth=data['warmth'],
        waterproof=data['waterproof'],
        level=data['level'],
        link=data['link']
    )
    db.session.add(gear)
    db.session.commit()

def get_gear(code):
    from ..db_models import Gear
    return Gear.query.get(code)

def insert_favourite(email, gearid):
    from ..db_models import db, FavouriteGear
    favourite = FavouriteGear(email=email, gearid=gearid)
    db.session.add(favourite)
    db.session.commit()

def get_favourites(email):
    from ..db_models import FavouriteGear
    return FavouriteGear.query.filter_by(email=email).all()

def add_user(email, name, lastname):
    from ..db_models import db, Users
    user = Users(email=email, name=name, lastname=lastname)
    db.session.add(user)
    db.session.commit()

def get_user_by_email(email):
    from ..db_models import FavouriteGear
    return FavouriteGear.query.filter_by(email=email).all()
"""