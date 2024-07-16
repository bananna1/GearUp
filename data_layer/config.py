import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '004f2af45d3a4e161a7dd2d17fdae47f'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False