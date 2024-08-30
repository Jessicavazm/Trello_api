from init import db, ma
from marshmallow import fields


# Create a new class for comments 
class Comment(db.Model):
    # Define name of the name
    __table__ = "comments"

    # Define the attributes
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), nullable=False)

    # Define relationship between FK and Comment model in order to get more info
    user = db.relationship("User", back_populates="comments")
    card = db.relationship("Card", back_populates="comments")


# Define Schema
# Unpack user 
class CommentSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    card = fields.Nested("CardSchema", exclude="comments")

    class Meta:
        fields = ["id", "message", "date", "user", "card"]


# Create objects for Comment
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)