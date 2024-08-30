# Import date to use method in the card objects
from datetime import date

# Import blueprint
from flask import Blueprint
# Import db from init
from init import db, bcrypt
from models.user import User
# Import Card to seed cards
from models.card import Card
from models.comment import Comment

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

    db.session.add_all(users)

    cards = [
        Card(
        title = "GitHub operations",
        description = "Perform mandatory github ops on the project",
        status = "To do",
        priority = "High priority",
        date = date.today(),
        user = users[0]
    ), Card(
        title = "Initialise the modules",
        description = "Perform init operations on the necessary modules",
        status = "On going",
        priority = "High priority",
        date = date.today(),
        user = users[0]

    ), Card(
        title = "Add comments to the code",
        description = "Add meaningful where necessary",
        status = "To do",
        priority = "Medium priority",
        date = date.today(),
        user = users[1]
    )]

    # Add and commit
    db.session.add_all(cards)

    # Create comments, date is set in the background
    # user_id is received by TOKEN
    # card_it is retrieve automatically from URL
    # Use Class name to create comments
    comments = [
        Comment(
            date = date.today(),
            user = users[0],
            card = cards[0],
            message = "Admin is making comment on Card 0"
        ),
        Comment (
            date = date.today(),
            user = users[0],
            card = cards[1],
            message = "Admin is making comment on Card 1"
        ),
        Comment (
            date = date.today(),
            user = users[1],
            card = cards[0],
            message = "User A is making comment on Card 0"
        )
    ]

    
    db.session.add_all(comments)

    db.session.commit()

    print("Tables seeded!")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped.")


