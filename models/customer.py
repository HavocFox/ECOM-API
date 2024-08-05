from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class Customer(Base):
    __tablename__ = 'Customers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    role_id = mapped_column(db.Integer, db.ForeignKey('Roles.id'), default=1)

    role: Mapped['Role'] = db.relationship()
    # One-to-Many: Customer and Order
    orders: Mapped[List["Order"]] = db.relationship(back_populates="customer")

   


