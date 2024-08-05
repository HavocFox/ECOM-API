from flask import Blueprint
from controllers.productController import save, find_all, search_product_by_id, update_product, delete_product

product_blueprint = Blueprint('product_bp', __name__)

product_blueprint.route('/', methods=['POST'])(save)
product_blueprint.route('/', methods=['GET'])(find_all)
product_blueprint.route('/<int:id>', methods=['GET'])(search_product_by_id)
product_blueprint.route('/update/<int:id>', methods=['PUT'])(update_product)
product_blueprint.route('/delete/<int:id>', methods=['DELETE'])(delete_product)
