from init import db, ma
# Import field to unpack nested fields
from marshmallow import fields


class Card(db.Model):
    # Set name for the table
    __tablename__ = "cards"

    # Define attributes
    id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    status = db.Column(db.String)
    priority = db.Column(db.String)
    date = db.Column(db.Date) # Created date

    # Define the Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # set relationship between user and cards
    user = db.relationship("User", back_populates= "cards")

# Create Schemas

class CardSchema(ma.Schema):
    # Unpack 'user' variable, use Schema from User.py and set fields required
    user = fields.Nested("UserSchema", only=["id", "name", "email"])

card_schema = CardSchema()
cards_schema = CardSchema(many=True)





