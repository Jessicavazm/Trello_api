from init import db,ma
# To unpack Nested fields import Fields
from marshmallow import fields
# Import Regexp for email validation
from marshmallow.validate import Regexp

class User(db.Model):
    # Name of the table
    __tablename__ = "users"

    # Attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Define relation to fetch more information from User and from Comment model
    cards = db.relationship("Card", back_populates = "user")
    comments = db.relationship("Comment", back_populates = "user")

# Create schema to serialize and deserialize data into python understandable data
# This extends from marshmallow schema, thats why you need to import ma first
class UserSchema(ma.Schema):
    # fields.List = you can receive more than one card per user
    # Unpack nested fields and exclude user, since you are fetching that info already 
    # Exclude 'user' in comments to break the loop
    # IF YOU WANT MORE INFO ABOUT RELATED TABLES, DEFINE THE RELATIONSHIP BETWEEN BOTH MODELS
    # USE THEIR MODELS SCHEMAS TO UNPACK AND THEN YOU WILL BE ABLE TO USE IT
    # AND THEN INCLUDE THEM IN THE META CLASS
    cards = fields.List(fields.Nested("CardSchema", exclude=["user"]))
    comments = fields.List(fields.Nested("CommentSchema", exclude=["user"]))
    
    email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="Invalid Email Format."))

    class Meta:
        fields = ("id", "name", "email", "password", "is_admin", "cards", "comments")


# Create objects to handle a single user object
user_schema = UserSchema(exclude=["password"])

# Create objects to handle a list of multiple users objects
users_schema = UserSchema(many=True, exclude=["password"])





