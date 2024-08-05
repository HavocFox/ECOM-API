from models.schemas.orderSchema import order_schema, orders_schema, order_item_schema, order_items_schema
from flask import request, jsonify
from marshmallow import ValidationError
from services import orderService
from utils.util import user_token_required, admin_required

# Creating/placing orders was considered the same as the function to checkout from cart, judging by the assignment description.

# ----- RETRIEVE ORDER BY ID -----
@user_token_required
def find_by_order_id(order_id, token_id):
    order, orderitems = orderService.find_by_order_id(order_id)
    if order is None:
        return jsonify({'message': 'Order not found'}), 404
    
    if order.customer_id == token_id:
        order_data = order_schema.dump(order)
        order_data['items'] = order_item_schema.dump(orderitems, many=True)  # Assuming you have an order_item_schema
        return jsonify(order_data), 200
    else:
        return jsonify({"messages": "You can't view other people's orders!"}), 401
