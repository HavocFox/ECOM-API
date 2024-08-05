from flask import request, jsonify
from models.schemas.productSchema import product_schema, products_schema
from services import productService
from marshmallow import ValidationError
from utils.util import admin_required

# ----- CREATE PRODUCT -----
@admin_required
def save():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    product_saved = productService.save(product_data)
    return product_schema.jsonify(product_saved), 201

# ----- LIST ALL PRODUCTS -----
def find_all():
    all_products = productService.find_all()
    return products_schema.jsonify(all_products), 200

# ----- READ PRODUCT BY ID -----
def search_product_by_id(id):
    product = productService.search_product_by_id(id)
    if product:
        return product_schema.jsonify(product), 200
    else:
        return jsonify({'message': 'Product not found'}), 404

# ----- UPDATE PRODUCT -----
@admin_required
def update_product(id):
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    updated_product = productService.update_product(id, product_data)
    if updated_product:
        return product_schema.jsonify(updated_product), 200
    else:
        return jsonify({'message': 'Product not found'}), 404

# ----- DELETE PRODUCT -----
@admin_required
def delete_product(id):
    result = productService.delete_product(id)
    if result:
        return jsonify({'message': 'Product deleted successfully'}), 200
    else:
        return jsonify({'message': 'Product not found'}), 404
