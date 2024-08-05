from marshmallow import fields
from . import ma

class OrderSchema(ma.Schema):
    id = fields.Integer(required=False)
    date = fields.Date(required=False)
    customer_id = fields.Integer(required=True)
    products = fields.Nested("ProductSchema", many=True)
    customer = fields.Nested("CustomerOrderSchema")
    
    class Meta:
        fields = ('id', 'date', 'customer_id', 'product_ids', 'products', 'customer')

class OrderItemSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    price = fields.Float(required=True)

# Create an instance of the OrderSchema
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)  # For handling multiple orders

order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)