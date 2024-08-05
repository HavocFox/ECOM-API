from flask import request, jsonify
from models.schemas.customerSchema import customer_schema, customers_schema, customer_update_schema, customer_delete_schema
from services import customerService
from marshmallow import ValidationError
from utils.util import admin_required, user_token_required, token_required

# ----- LOG IN -----
def login():
    try:
        credentials = request.json
        token = customerService.login(credentials['username'], credentials['password'])
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting username and password'}), 401
    
    if token:
        return jsonify(token), 200
    else:
        return jsonify({'messages': "Invalid username or password"}), 401

# ----- CREATE CUSTOMER -----
def save():
    try:
        customer_data = request.json
        customer_data = customer_schema.load(customer_data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_customer = customerService.save(customer_data)
    return customer_schema.jsonify(new_customer), 201

# ----- FIND ALL CUSTOMERS -----
@admin_required
def find_all():        
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    customers = customerService.find_all(page, per_page)
    return customers_schema.jsonify(customers), 200

# ----- READ CUSTOMER BY ID -----
@user_token_required
def search_customer_by_id(token_id, id):
    if id == token_id:
        customer = customerService.search_customer_by_id(id)
        if customer:
            return customer_schema.jsonify(customer), 200
        else:
            return jsonify({'message': 'Customer not found'}), 404
    else:
        return jsonify({'message':"You can't view others' profiles!"})

# ----- UPDATE CUSTOMER -----
# You can only update your own profile.
@user_token_required
def update_customer(token_id, id):
    if id == token_id:
        try:
            customer_data = request.json
            customer_data = customer_update_schema.load(customer_data)
        except ValidationError as e:
            return jsonify(e.messages), 400

        updated_customer = customerService.update_customer(id, customer_data)
        if updated_customer:
            return customer_schema.jsonify(updated_customer), 200
        else:
            return jsonify({'message': 'Customer not found'}), 404
    else:
        return jsonify({'message':" You can't update others' profiles!"})


# ----- DELETE CUSTOMER -----
# You must be an admin to do this. Personal choice not to let logged in customers delete themselves.
@admin_required
def delete_customer(id):
    result = customerService.delete_customer(id)
    if result:
        return jsonify({'message': 'Customer deleted successfully'}), 200
    else:
        return jsonify({'message': 'Customer not found'}), 404
