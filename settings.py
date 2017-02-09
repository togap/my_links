import os

base_dir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'my_links.db')
