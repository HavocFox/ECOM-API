from models.order import Order, OrderItem
from models.product import Product
from models.customer import Customer
from datetime import date
from sqlalchemy import select
from database import db
from utils.util import admin_required, user_token_required, token_required


def find_by_order_id(order_id):
    # Query to find the order by its ID
    query = select(Order).where(Order.id == order_id)
    order = db.session.execute(query).scalar_one_or_none()

    # Query to find all order items associated with the order
    query = select(OrderItem).where(OrderItem.order_id == order_id)
    orderitems = db.session.execute(query).scalars().all()  # Fetch all matching rows

    return order, orderitems


# Exclusively for use by the controller function (no user endpoint)
def find_products_by_order_id(order_id):
    query = select(OrderItem).where(OrderItem.order_id == order_id)
    orderitems = db.session.execute(query).scalars().all()
    return orderitems
