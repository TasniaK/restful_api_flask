import os
basedir = os.path.abspath(os.path.dirname(__file__))

# A class to store config vars, in a separate module - separation of concerns.
# Using SQLite.
# NOTE: go over where to set env vars.
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'restful_api_project.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False