from database import db
from models.customer import Customer
from models.cart import Carts
from sqlalchemy import select
from utils.util import encode_token
from models.schemas.customerSchema import customer_update_schema

def login(email, password):
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalar_one_or_none()

    if customer and customer.password == password:
        auth_token = encode_token(customer.id, customer.role.role_name)
        response = {
            'status': "success",
            'message': "Logged in successfully.",
            'auth_token': auth_token
        }
        return response
    return None




def save(customer_data):
    new_customer = Customer(
        email=customer_data['email'],
        phone=customer_data['phone'],
        password=customer_data['password'],
    )
    db.session.add(new_customer)
    db.session.commit()

    return new_customer





def find_all(page, per_page):
    customers = db.paginate(select(Customer), page=page, per_page=per_page)
    return customers

def search_customer_by_id(id):
    query = select(Customer).where(Customer.id == id)
    customer = db.session.execute(query).scalar_one_or_none()
    return customer


# Might not use this. Not a desperately needed feature
def update_customer(id, customer_data):
    query = select(Customer).where(Customer.id == id)
    updated_customer = db.session.execute(query).scalar_one_or_none()
    if updated_customer:
        updated_customer.email = customer_data['email']
        db.session.commit()
        return updated_customer
    return None

def delete_customer(id):
    query = select(Customer).where(Customer.id == id)
    customer_to_delete = db.session.execute(query).scalar_one_or_none()
    if customer_to_delete:
        db.session.delete(customer_to_delete)
        db.session.commit()
        return True
    return False
