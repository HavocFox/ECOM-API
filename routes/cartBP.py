from flask import Blueprint
from controllers.cartController import add_to_cart, remove_from_cart, view_cart, empty_cart, proceed_to_checkout

cart_blueprint = Blueprint('cart_bp', __name__)

cart_blueprint.route('/add', methods=['POST'])(add_to_cart)
cart_blueprint.route('/<int:cart_id>/delete/<int:item_id>', methods=['DELETE'])(remove_from_cart)
cart_blueprint.route('/<int:id>', methods=['GET'])(view_cart)
cart_blueprint.route('/empty/<int:cart_id>', methods=['DELETE'])(empty_cart)
cart_blueprint.route('/checkout/<int:cart_id>', methods=['POST'])(proceed_to_checkout)
