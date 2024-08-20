# Import blueprint and request method to access data
from flask import Blueprint, request
# Import User to create an instance, bcrypt for hash and db to use database
from models.user import User, user_schema
from init import bcrypt, db
# Import IntegrityError
from sqlalchemy.exc import IntegrityError
# Import error codes from psycopg
from psycopg2 import errorcodes

# Create blueprint with url_prefix
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

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


