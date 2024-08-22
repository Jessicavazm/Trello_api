from init import db,ma
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

    # Mention relationship
    cards = db.relationship("Card", back_populates = "user")

# Create schema to serialize and deserialize data into python understandable data
# This extends from marshmallow schema, thats why you need to import ma first
class UserSchema(ma.Schema):
    class Meta:
        #Fields
        cards = fields.List(fields.Nested("CardSchema", exclude=["user"]))
        fields = ("id", "name", "email", "password", "is_admin", "cards")

# Create objects to handle a single user
user_schema = UserSchema(exclude=["password"])
# Create objects to handle a list of multiple users 
users_schema = UserSchema(many=True, exclude=["password"])





