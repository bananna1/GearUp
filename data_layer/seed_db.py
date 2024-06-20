import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from db_models import db, Gear

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    return app

app = create_app()

@app.cli.command('seed_db')
def seed_db():
    """Seed the database with initial data"""
    with open('gear_data.json') as f:
        gear_data = json.load(f)
        for item in gear_data:
            gear = Gear(
                code=item['code'],
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

if __name__ == '__main__':
    app.run(debug=True)