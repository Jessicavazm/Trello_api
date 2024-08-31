# Import the Database and marshmallow
from init import db, ma
# Import 'fields' to unpack complex data type = nested fields
# Decorator 'validate' register a field 
from marshmallow import fields, validates
# Import Length class for validation, And = combine validation, Regexp = ensure validations
# OneOF validate status, it allows users to select one of the options
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

# Define a constant by UPPER CASE LETTER
VALID_STATUSES = ("To Do", "In Progress", "Completed", "Testing", "Deployed")
VALID_PRIORITIES = ("Low", "Medium", "High", "Immediate")


# Create the Card model, it takes reference from the db.Model 
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
    # Back_populates allows User model to fetch information from Card model.
    # When you want to fetch more info than FK, you define relationship and then unpack nested fields.
    # Use CASCADE in comments to make sure if a card is deleted, the comments are also deleted
    user = db.relationship("User", back_populates= "cards")
    comments = db.relationship("Comment", back_populates="card", cascade="all, delete")


# Create Schemas
# Use fields.Nested because you expect a list of items
# Tell the Schema, user is not a normal field, it's nested
class CardSchema(ma.Schema):
    # Unpack 'user' variable, use Schema from User.py and set fields required
    # Use 'UserSchema' in the parameter since this schema already knows how to unpack these values
    # Use 'only' to select required fields
    user = fields.Nested("UserSchema", only=["id", "name", "email"])
    comments = fields.List(fields.Nested("CommentSchema", exclude = ["card"]))
    
    # Validation on 'title'
    # required=True gives an extra layer of security, it makes reference to 'title = nullable=False'
    # AND combine two validation requests (length and RegeXP = regular expression)
    title = fields.String(required=True, validate=And(Length(min=4, error="Title must be at least 4 characters in length."), Regexp('^[A-Z][A-Za-z0-9 ]+$', error="Title must start with upper case letter and have alphanumeric characters only.")))

    # Implements the 'status' and 'priority' validation
    status = fields.String(validate=OneOf(VALID_STATUSES))
    priority = fields.String(validate=OneOf(VALID_PRIORITIES, error= "Invalid Priority Selected"))

    # Use @decorator to validate fields, every time you see a decorator, you define a function for it
    @validates("status")
    # 'self' initialise the 'value'
    def validate_status(self, value):
        # if trying to see the value of status as "In Progress"
        if value == VALID_STATUSES[1]:
            # check whether an existing In Progress card exists or not
            # SELECT COUNT(*) FROM table_name WHERE status="In Progress"
            stmt = db.select(db.func.count()).select_from(Card).filter_by(status=VALID_STATUSES[1])
            count = db.session.scalar(stmt)
            # if it exists
            if count > 0:
                # send error message
                raise ValidationError("You already have an In-Progress card.")
    
    class Meta:
        fields = ("id", "title", "description", "status", "priority", "date", "user", "comments")
        # Display fields in the order
        ordered = True

card_schema = CardSchema()
cards_schema = CardSchema(many=True)





