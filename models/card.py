# Import the Database and marshmallow
from init import db, ma
# Import 'fields' to unpack complex data type = nested fields
from marshmallow import fields

# Create the Card class, it takes reference from the db.Model 
class Card(db.Model):
    # Define name for the table
    __tablename__ = "cards"

    # Define attributes
    id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    status = db.Column(db.String)
    priority = db.Column(db.String)
    date = db.Column(db.Date) # Created date

    # Include FK. Define the Foreign Key
    # db.ForeignKey(name of the table + column name)
    # Fetch user ID attribute from table 'Users'
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Define a relationship between user and cards, to fetch more info about user
    # This value doesn't come directly from DB, SQLAlchemy fetch this information and sends it
    # db.relation(Model_name, back_populates = field)
    # Back_populates allows User model to fetch information from Cards table.
    # When you want to fetch more info than FK, you define relationship and then unpack nested fields.
    user = db.relationship("User", back_populates= "cards")

# Create Schemas
# Use fields.Nested because you expect a list of items
# Tell the Schema, user is not a normal field, it's nested
class CardSchema(ma.Schema):
    # Unpack 'user' variable, use Schema from User.py and set fields required
    # Use 'UserSchema' in the parameter since this schema already knows how to unpack these values
    # Use 'only' to select required fields
    user = fields.Nested("UserSchema", only=["id", "name", "email"])
    
    class Meta:
        fields = ("id", "title", "description", "status", "priority", "date", "user")


card_schema = CardSchema()
cards_schema = CardSchema(many=True)





