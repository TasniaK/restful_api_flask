from restful_api_app import app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# NOTE: not sure I need to reinstantiate the app.
app.config.from_object(Config)

# Represents the db as an object.
db = SQLAlchemy(app)
# Represents the migration engine as an object.
migrate = Migrate(app, db)

# models (classes) module defines the structure of the db.
from models import Task