from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.cartproduct import cart_product
from models.cart import Carts

class Product(Base):
    __tablename__ = 'Products'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    carts: Mapped[List[Carts]] = relationship(secondary=cart_product, back_populates='products')
