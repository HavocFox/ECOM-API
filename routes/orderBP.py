from flask import Blueprint
from controllers.orderController import find_by_order_id

order_blueprint = Blueprint('order_bp', __name__)

order_blueprint.route('/<int:order_id>', methods=['GET'])(find_by_order_id)
