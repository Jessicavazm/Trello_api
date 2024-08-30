# Import OS to fetch env variables 
import os
# Have the core python(flask) code for app 
# Import flask class from Flask package 
# Import blueprint from controllers folder
from flask import Flask
from controllers.cli_controllers import db_commands
# Import objects from init.py and use them
from init import db, ma, bcrypt, jwt
# Import auth_bp and cards_bp to register it in main.py
from controllers.auth_controller import auth_bp
from controllers.card_controller import cards_bp


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

    # Register blueprint to use db_commands, auth_bp, cards_bp
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cards_bp)

    return app
