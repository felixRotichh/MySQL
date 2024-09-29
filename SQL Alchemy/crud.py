from database import get_session
from models import Customer, Product, Order, OrderItem

# Create new Customer
def create_customer(name: str, email: str) -> None:
    session = get_session()
    new_customer = Customer(name=name, email=email)
    session.add(new_customer)
    session.commit()
    session.close()

# Create new Product
def create_product(name: str, price: float, stock: int) -> None:
    session = get_session()
    new_product = Product(name=name, price=price, stock=stock)
    session.add(new_product)
    session.commit()
    session.close()

# Create new Order with Product items
def create_order(customer_id: int, product_quantities: dict[str, int]) -> None:
    session = get_session()
    
    # Retrieve all products to avoid multiple queries
    products = {product.name: product for product in session.query(Product).all()}
    
    # Create the order for the customer
    order = Order(customer_id=customer_id)
    session.add(order)
    session.commit()

    # Create order items based on product names and quantities
    for product_name, quantity in product_quantities.items():
        product = products.get(product_name)
        if product:
            order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity)
            session.add(order_item)
        else:
            print(f"Product '{product_name}' not found")
    
    # Recalculate total after adding order items
    order.calculate_total()
    session.commit()
    session.close()

# Reading from the database
def get_customers():
    session = get_session()
    customers = session.query(Customer).all()
    session.close()
    return customers

def get_products():
    session = get_session()
    products = session.query(Product).all()
    session.close()
    return products

def get_orders():
    session = get_session()
    orders = session.query(Order).all()
    session.close()
    return orders

# Update a Product's price
def update_product_price(product_id: int, new_price: float) -> None:
    session = get_session()
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        product.price = new_price
        session.commit()
    session.close()

# Update stock
def update_product_stock(product_id: int, new_stock: int) -> None:
    session = get_session()
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        product.stock = new_stock
        session.commit()
        print(f"Stock updated for product ID {product_id}")
    else:
        print(f"Product with ID {product_id} not found.")
    session.close()


# Delete a Customer
def delete_customer(customer_id: int) -> None:
    session = get_session()
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer:
        session.delete(customer)
        session.commit()
    session.close()
