from models.product import Product
from database import db
from sqlalchemy import select

def save(product_data):
    new_product = Product(name=product_data['name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    db.session.refresh(new_product)
    return new_product

def find_all():
    query = select(Product)
    all_products = db.session.execute(query).scalars().all()
    return all_products

def search_product_by_id(id):
    query = select(Product).where(Product.id == id)
    product = db.session.execute(query).scalar_one_or_none()
    return product

def update_product(id, product_data):
    query = select(Product).where(Product.id == id)
    updated_product = db.session.execute(query).scalar_one_or_none()
    if updated_product:
        updated_product.name = product_data['name']
        updated_product.price = product_data['price']
        db.session.commit()
        return updated_product
    return None

def delete_product(id):
    query = select(Product).where(Product.id == id)
    product_to_delete = db.session.execute(query).scalar_one_or_none()
    if product_to_delete:
        db.session.delete(product_to_delete)
        db.session.commit()
        return True
    return False
