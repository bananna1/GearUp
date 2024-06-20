from db_models import db, Gear, FavouriteGear

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
    return Gear.query.get(code)

def insert_favourite(email, gearid):
    favourite = FavouriteGear(email=email, gearid=gearid)
    db.session.add(favourite)
    db.session.commit()

def get_favourites(email):
    return FavouriteGear.query.filter_by(email=email).all()
