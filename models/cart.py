from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
from models.cartproduct import cart_product

class Item(Base):
    __tablename__ = 'Items'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    quantity: Mapped[float] = mapped_column(db.Float, nullable=False)
    cart_id: Mapped[int] =  mapped_column(db.Integer, db.ForeignKey('Carts.id'))
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

class Carts(Base):
    __tablename__ = 'Carts'
    id: Mapped[int] = mapped_column(primary_key=True)
    # Many to many relationship between Carts and Products
    products: Mapped[List["Product"]] = db.relationship(secondary=cart_product, back_populates='carts')
    total_price: Mapped[float] = mapped_column(db.Float, nullable=False)
