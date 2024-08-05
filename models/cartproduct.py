from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import db, Base

cart_product = db.Table(
    'cart_product',
    Base.metadata,
    db.Column('cart_id', db.ForeignKey('Carts.id'), primary_key=True),
    db.Column('product_id', db.ForeignKey('Products.id'), primary_key=True)
)
