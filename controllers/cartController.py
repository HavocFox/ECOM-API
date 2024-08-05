from flask import request, jsonify
from models.schemas.cartSchema import cart_item_schema, cart_schema
from services import cartService
from marshmallow import ValidationError
from utils.util import user_token_required, admin_required

# ----- ADD TO CART -----
@user_token_required
def add_to_cart(token_id):
    try:
        item_to_add = request.json
    except KeyError:
        return jsonify({"message": "Invalid data format. 'cart_id', 'product_id' and 'quantity' keys are required."}), 400
    
    if item_to_add['cart_id']== token_id:
        try:
            valid, message = cartService.add_to_cart(item_to_add)
            if not valid:
                return jsonify({"message": message}), 400
            return jsonify({"message": message}), 201
    
        except ValidationError as e:
            return jsonify(e.messages), 400
    else:
        return jsonify({'message':"You can't add things to other peoples' carts!"})

# ----- REMOVE FROM CART -----
@user_token_required
def remove_from_cart(token_id, cart_id, item_id):
    if cart_id == token_id:
        success, message = cartService.remove_item(cart_id, item_id)
    
        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": message}), 400
    else:
        return jsonify({'message':"You can't remove things from other peoples' carts!"})

# ----- VIEW CART -----
@user_token_required
def view_cart(token_id, id):
    if token_id == id:
        success, cart = cartService.view_cart(id)
        if success:
            return jsonify(cart), 200
        else:
            return jsonify({"message": "Cart not found"}), 404
    else:
        return jsonify({'message':"You can't view other peoples' carts!"})

# ----- EMPTY CART -----
@user_token_required
def empty_cart(token_id, cart_id):
    if token_id == cart_id:
        data = request.json
        confirmation = data.get('confirmation', False)
        success, message = cartService.empty(cart_id, confirmation)
        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": message}), 400
    else:
        return jsonify({'message':"You can't empty other peoples' carts!"})

# ----- PROCEED TO CHECKOUT -----
@user_token_required
def proceed_to_checkout(token_id, cart_id):
    if token_id == cart_id:
        result = cartService.checkout(cart_id)
        if result:
            return jsonify({"message": "Order placed successfully"}), 200
        else:
            return jsonify({"message": "Failed to place order"}), 400
    else:
        return jsonify({'message':"You can't checkout other peoples' carts!"})
