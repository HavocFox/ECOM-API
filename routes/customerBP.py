from flask import Blueprint
from controllers.customerController import save, find_all, login, search_customer_by_id, update_customer

customer_blueprint = Blueprint('customer_bp', __name__)

customer_blueprint.route('/add', methods=['POST'])(save)
customer_blueprint.route('/', methods=['GET'])(find_all)        # Keeping for now. Might need to remove from final but should be nice to have for debug.
customer_blueprint.route('/<int:id>', methods=['GET'])(search_customer_by_id)
customer_blueprint.route('/update/<int:id>', methods=['PUT'])(update_customer)
customer_blueprint.route('/login', methods=['POST'])(login)
