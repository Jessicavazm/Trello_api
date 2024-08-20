# Import blueprint
from flask import Blueprint
# Import db from init
from init import db, bcrypt
from models.user import User

# Define an object
db_commands = Blueprint("db", __name__)

# Use blueprint to create CLI commands
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("seed")
def seed_tables():
    # Create a list of User instances and hash password using bcrypt
    users = [
        User(
            email = "admin@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8"),
            is_admin = True
        ), 
        User(
            name = "User A",
            email = "usera@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8")
        )
    ]

    # Add and commit
    db.session.add_all(users)

    db.session.commit()

    print("Tables seeded!")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped.")


