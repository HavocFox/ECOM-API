from marshmallow import fields
from . import ma

# What we will be feeding to the cart

class CartItemSchema(ma.Schema):
    cart_id = fields.Integer(required=True)
    item_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    
    class Meta:
        fields = ('id', 'name', 'price', 'item', 'quantity', 'total_price', 'cart_id', 'items')
 
class CartSchema(ma.Schema):
    id = fields.Integer(required=False)
    total_price = fields.Float(required=True)
    items = fields.List(fields.Nested(CartItemSchema), required=True)

class CartItemRemoveSchema(ma.Schema):
    cart_id = fields.Integer(required=True)
    item_id = fields.Integer(required=True)

cart_item_schema = CartItemSchema()
cart_schema = CartSchema()