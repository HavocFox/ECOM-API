from typing import List
from datetime import datetime
from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from models.orderproduct import order_product

class Order(Base):
    __tablename__ = 'Orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('Customers.id'))
    total_price: Mapped[float] = mapped_column(db.Float, nullable=False)
    
    # Many-To-One: Order and Customer     
    customer: Mapped["Customer"] = db.relationship("Customer", back_populates="orders")
    
    # One-To-Many: Order and OrderItem
    items: Mapped[List["OrderItem"]] = db.relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(db.ForeignKey('Orders.id'))
    product_id: Mapped[int] = mapped_column(db.Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

    # Many-To-One: OrderItem and Order
    order: Mapped["Order"] = db.relationship("Order", back_populates="items")
