from init import db,ma
# To unpack Nested fields import Fields
from marshmallow import fields

class User(db.Model):
    # Name of the table
    __tablename__ = "users"

    # Attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Define relation to fetch more information from User 
    cards = db.relationship("Card", back_populates = "user")

# Create schema to serialize and deserialize data into python understandable data
# This extends from marshmallow schema, thats why you need to import ma first
class UserSchema(ma.Schema):
    class Meta:
        # fields.List = you can receive more than one card per user
        # Unpack nested fields and exclude user, since you are fetching that info already 
        cards = fields.List(fields.Nested("CardSchema", exclude=["user"]))
        fields = ("id", "name", "email", "password", "is_admin", "cards")

# Create objects to handle a single user
user_schema = UserSchema(exclude=["password"])
# Create objects to handle a list of multiple users 
users_schema = UserSchema(many=True, exclude=["password"])





