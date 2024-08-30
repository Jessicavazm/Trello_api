# Import blueprint and request method to access data
from flask import Blueprint, request
# Import User to create an instance, bcrypt for hash and db to use database
from models.user import User, user_schema
from models.comment import Comment
from init import bcrypt, db
# Import IntegrityError
from sqlalchemy.exc import IntegrityError
# Import error codes from psycopg
from psycopg2 import errorcodes
# Import create_access_token to create Token and timedelta for expire date
from flask_jwt_extended import create_access_token
from datetime import timedelta

# Create blueprint with url_prefix
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Create the Register route
@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:    
        # Get the data from the body of the request and store it in a variable
        body_data = request.get_json()
        # Create an instance of the User model to storage data
        user = User(
            name = body_data.get("name"),
            email = body_data.get("email"),
        )
        # Step for handling sensitive information, hash the password.
        # Use 'IF' for validation, SQLAlchemy automatically handles if password doesn't exist
        password = body_data.get("password")
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # Add and commit to the DB
        db.session.add(user)
        db.session.commit()
        # Return acknowledgement back to the user, dump converts Python to Dictionary
        return user_schema.dump(user), 201
    # Use personalized error messages with Psycopg
    # {err.orig.diag.column_name} Fetches the specific column name where there is an error
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address must be unique"}, 400


# Create the LOGIN route
@auth_bp.route("/login", methods=["POST"])
def login_user():
    # Get the data from the body of the request
    body_data = request.get_json()
    # Find the user in database with that email address using stmt
    # stmt = path to fetch info 
    stmt = db.select(User).filter_by(email=body_data["email"]) 
    # Execute the stmt
    user = db.session.scalar(stmt)
    # If user exist and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # Create JWT
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        # Send JWT back to user
        return {"email": user.email, "is_admin": user.is_admin, "token": token}
    # Else
    else:
        # Respond back with message
        return {"error": "Invalid email or password"}, 400
        

