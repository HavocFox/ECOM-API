from database import db
from models.cart import Carts, Item
from models.product import Product
from datetime import datetime
from models.order import Order, OrderItem
from sqlalchemy import select
from sqlalchemy.orm import aliased
from marshmallow import ValidationError
from models.schemas.cartSchema import cart_item_schema
from models.cartproduct import cart_product

import logging      # Personal DEBUG stuff to tell where things are going wrong.
logging.basicConfig(level=logging.INFO)

def add_to_cart(item_data):
    current_cart_id = item_data['cart_id']

    # Fetch the product
    query = select(Product).where(Product.id == item_data['item_id'])
    current_product = db.session.execute(query).scalar_one_or_none()

    # Fetch the cart
    query = select(Carts).where(Carts.id == current_cart_id)
    current_cart = db.session.execute(query).scalar_one_or_none()

    # Check if the product exists
    if current_product is None:
        return False, "Product with the given item_id does not exist."

    # Check if the cart exists
    if current_cart is None:
        return False, "Cart with the given cart_id does not exist."


    # Check if the item already exists in the cart
    query = select(Item).where(Item.cart_id == current_cart_id, Item.product_id == item_data['item_id'])
    existing_item = db.session.execute(query).scalar_one_or_none()

    if existing_item:
        # If item exists, update the quantity
        existing_item.quantity += item_data['quantity']
        db.session.commit()
        return True, "Item quantity updated in cart."
    else:
        # Create a new cart item
        new_cart_item = Item(
            product_id=current_product.id,
            price=current_product.price,
            cart_id=current_cart_id,
            quantity=item_data['quantity'],
        )
        db.session.add(new_cart_item)
        db.session.commit()

    new_cart_item = cart_product.insert().values(cart_id=current_cart_id, product_id=item_data['item_id'])
    db.session.execute(new_cart_item)
    db.session.commit()

    # Update the cart's total price
    current_cart.total_price = current_cart.total_price + current_product.price*item_data['quantity']
    db.session.commit()

    return True, "Item added to cart successfully."


def remove_item(cart_id, item_id):

    # Fetch the cart
    query = select(Carts).where(Carts.id == cart_id)
    current_cart = db.session.execute(query).scalar_one_or_none()

    query = select(Item)
    all_items = db.session.execute(query).scalars().all()

    query = select(Item).where(Item.cart_id == cart_id, Item.product_id == item_id)
    item_to_remove = db.session.execute(query).scalar_one_or_none()
    
    if item_to_remove:
        db.session.delete(item_to_remove)
        db.session.commit()

        query = select(Product).where(Product.id == item_to_remove.product_id)
        current_product = db.session.execute(query).scalar_one_or_none()

        remove_from_cartprod = cart_product.delete().where(cart_product.c.cart_id == cart_id, cart_product.c.product_id == item_id)
        db.session.execute(remove_from_cartprod)
        db.session.commit()

        current_cart.total_price = current_cart.total_price - current_product.price*item_to_remove.quantity
        db.session.commit()
        return True, f"Item ID {item_id} removed from cart ID {cart_id}."

    return False, f"Couldn't find item ID {item_id} in cart {cart_id}."


def view_cart(id):
    query = select(Carts).where(Carts.id == id)
    current_cart = db.session.execute(query).scalar_one_or_none()
    
    if current_cart:
        cart_items_query = select(Item).where(Item.cart_id == id)
        cart_items = db.session.execute(cart_items_query).scalars().all()
        
        product_display = []
        for item in cart_items:
            product_query = select(Product).where(Product.id == item.product_id)
            product = db.session.execute(product_query).scalar_one_or_none()
            
            if product:
                product_display.append(f"Product: {product.name}, Quantity: {item.quantity}, Price: {item.price} .... ")
        
        cart_summary = {
            "cart_id": id,
            "items": " ".join(product_display),
            "total_price": current_cart.total_price
        }
        
        return True, cart_summary
    
    return False, None



def empty(cart_id, confirmation):
    if not confirmation:
        return False, "Confirmation required to empty the cart."
    
    # Fetch the cart
    query = select(Carts).where(Carts.id == cart_id)
    current_cart = db.session.execute(query).scalar_one_or_none()

    if current_cart:
        db.session.query(Item).filter_by(cart_id=cart_id).delete()
        db.session.commit()

        db.session.query(cart_product).filter_by(cart_id=cart_id).delete()
        db.session.commit()

        # Reset the total price
        current_cart.total_price = 0
        db.session.commit()

        return True, "Cart emptied successfully."
    
    return False, "Cart not found."

def checkout(cart_id):
    # Fetch the cart
    query = select(Carts).where(Carts.id == cart_id)
    current_cart = db.session.execute(query).scalar_one_or_none()

    counter = 0
    
    if not current_cart:
        return False, "Cart not found."



    # Create a new order
    new_order = Order(
        customer_id=cart_id,
        order_date=datetime.now(),
        total_price=current_cart.total_price
    )
    db.session.add(new_order)
    db.session.commit()

    query = select(Item).where(Item.cart_id == cart_id)
    cart_items = db.session.execute(query).scalars().all()
    
    for item in cart_items:     # do we have items in the cart?
        counter = counter + 1
    if counter == 0:
        return False, "No items in cart."

# Add items from the cart to the order
    for item in cart_items:
        item_add = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.session.add(item_add)

    db.session.commit()

    # Empty the cart
    db.session.query(Item).filter_by(cart_id=cart_id).delete()
    current_cart.total_price = 0
    db.session.commit()

    # remove the cart items from cart product assoc. table
    db.session.query(cart_product).filter_by(cart_id=cart_id).delete()
    db.session.commit()

    return True, "Order placed successfully."

def validate_items(items):
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    product_map = {product.name.lower(): product for product in products}

    for item in items:
        if item['name'].lower() not in product_map:
            return False, item['name'], None
    return True, None, product_map

def process_items(items_data, customer_id):
    valid, invalid_item_name, product_map = validate_items(items_data)
    if not valid:
        return False, invalid_item_name, None

    for item_data in items_data:
        current_request = cart_item_schema.load(item_data)
        current_request['price'] = product_map[current_request['name'].lower()].price
        current_request['cart_id'] = customer_id
    return True, current_request, product_map
