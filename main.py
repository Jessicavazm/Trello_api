# Import OS to fetch env variables 
import os
# Have the core python(flask) code for app 
# Import flask class from Flask package
from flask import Flask

# Import objects from init.py and use them
from init import db, ma, bcrypt, jwt

# Wrap the app definition inside of a function = application factories
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # Initialise objects
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    return app
