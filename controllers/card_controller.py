from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.card import Card, card_schema, cards_schema

# Create a blueprint and register it in main file.
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# /cards - GET - fetch all cards default = ' / '
# Default method is GET, no need to explicit
@cards_bp.route("/")
def get_all_cards():
    # Create and execute stmt, order by descending order
    stmt = db.select(Card).order_by(Card.date.desc())
    # scalar for a singular value, scalars for multiple values
    cards = db.session.scalars(stmt)
    # return cards, 
    # Deserialise using cards_schemas.dump
    return cards_schema.dump(cards)


# /cards/<id> - GET - fetch specific card
@cards_bp.route("/<int:card_id>")
def get_a_card(card_id):
    # Use filter_by to select a specific card
    # stmt = db.select(Card).where(Card.id==card_id)
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    if card:
        return card_schema.dump(card)
    else:
        return {"error": f"Card with {card_id} not found."}, 404
    
    
# /cards - POST - create a new card
@cards_bp.route("/", methods=["POST"])
# Requires token
@jwt_required()
def create_card():
    # Get the data from the body of the request
    card_body = request.get_json()
    # Create a new card model instance
    # user_id is a foreign key in this table
    # Get user_id from token
    card = Card(
        title = card_body.get("title"),
        description = card_body.get("description"),
        date = date.today(),
        status = card_body.get("status"),
        priority = card_body.get("priority"),
        user_id = get_jwt_identity()
    )
    # Add and commit to DB
    db.session.add(card)
    db.session.commit()
    # Response message
    return card_schema.dump(card), 201
    

# /cards/<id> - DELETE - delete a card
@cards_bp.route("/<int:card_id>", methods=["DELETE"])
@jwt_required()
def delete_card(card_id):
    # Fetch the card from DB
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    # If card exist
    if card:    
        # Delete the card
        db.session.delete(card)
        db.session.commit()
        return {"message": f"Card {card.title} deleted successfully!"}
    # Else
    else:
        # Return error message
        return {"error": f"Card {card_id} not found."}, 404
    
    
# /cards/<id> - PUT, PATCH - edit a card entry
@cards_bp.route("/<int:card_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_card(card_id):
    # get the info from the body of the request
    body_data = request.get_json()
    # get the card from the database
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    # if the card exists
    if card:
        # update the fields as required
        card.title = body_data.get("title") or card.title
        card.description = body_data.get("description") or card.description
        card.status = body_data.get("status") or card.status
        card.priority = body_data.get("priority") or card.priority
        # commit to the DB
        db.session.commit()
        # return acknowledgement
        return card_schema.dump(card)
    # else
    else:
        # return error message
        return {"error": f"Card with id {card_id} not found."}, 404