import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy import insert
from sqlalchemy.ext.declarative import declarative_base
from config import Config

from app import app



basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)

Base = declarative_base()

engine = create_engine('sqlite:///' + os.path.join(basedir, 'database.db'), echo = True)


class Gear(Base):  
    __tablename__ = "gear"
    code = Column("code", Integer, primary_key=True, nullable=False)
    description = Column("description", String, nullable=False)
    gender = Column("gender", CHAR, nullable=False)
    category = Column("category", String, nullable=False)
    warmth = Column("warmth", String, nullable=False)
    waterproof = Column("waterproof", Integer, nullable=False)
    level = Column("level", String, nullable=False)
    link = Column("link", String, nullable=False)

    def __init__(self, code, description, gender, category, warmth, waterproof, level, link):
        self.code = code
        self.description = description
        self.gender = gender
        self.category = category
        self.warmth = warmth
        self.waterproof = waterproof
        self.level = level
        self.link = link
    
    def __repr__(self):
        return f"{self.code}: {self.description}, {self.gender}, {self.category}, {self.warmth}, {self.waterproof}, {self.level}, {self.link}"


class Users(Base):
    __tablename__ = "users"
    email = Column("email", String, primary_key=True, nullable=False)
    id = Column("id", Integer, autoincrement=True)
    name = Column("name", String, nullable=False)
    lastname = Column("lastname", String, nullable=False)

class FavouriteGear(Base):
    __tablename__ = "favourite_gear"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String,ForeignKey("users.email"), nullable=False)
    gearid = Column("gearid", Integer, ForeignKey("gear.code"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('email', 'gearid', name='unique_favourite_gear'),
    )

    def __init__(self, email, gearid):
        self.email = email
        self.gearid = gearid
    
    def __repr__(self):
        return f"{self.email}: {self.gearid}"
    
class FavouriteTrails(Base):
    __tablename__ = "favourite_trails"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    Column("email", String,ForeignKey("users.email"), nullable=False)
    trailid = Column("trailid", Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('email', 'trailid', name='unique_favourite_trail'),
    )

    def __init__(self, email, gearid):
        self.email = email
        self.gearid = gearid
    
    def __repr__(self):
        return f"{self.email}: {self.gearid}"

