from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, func, Index
from sqlalchemy.orm import declarative_base, relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property

# Defining base class
Base = declarative_base()

__all__ = ['Customer', 'Product', 'Order', 'OrderItem']

# Customer Model
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())  # Automatically set when record is created
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())  # Update on record change

    orders = relationship('Order', back_populates='customer')

    def __repr__(self):
        return f"<Customer(id={self.id}, name={self.name}, email={self.email})>"
    __table_args__ = (
        Index('ix_customer_email', 'email'),
    )

    def __repr__(self):
        return f"<Customer(id={self.id}, name={self.name}, email={self.email})>"

    def __str__(self):
        return self.__repr__()

# Product Model
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    order_items = relationship('OrderItem', back_populates='product')

    __table_args__ = (
        Index('ix_product_name', 'name'),
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, stock={self.stock})>"

    def __str__(self):
        return self.__repr__()

    @validates('price')
    def validate_price(self, key, value):
        assert value >= 0, "Price must be non-negative"
        return value

    @validates('stock')
    def validate_stock(self, key, value):
        assert value >= 0, "Stock must be non-negative"
        return value

# Order Model
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    total_amount = Column(Numeric(10, 2), default=0.0, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    customer = relationship('Customer', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_order_customer_id', 'customer_id'),
    )

    def __repr__(self):
        return f"<Order(id={self.id}, customer_id={self.customer_id}, total_amount={self.total_amount})>"

    def __str__(self):
        return self.__repr__()

    @hybrid_property
    def calculated_total_amount(self):
        return sum(item.quantity * item.product.price for item in self.order_items)

    @validates('total_amount')
    def validate_total_amount(self, key, value):
        assert value >= 0, "Total amount must be non-negative"
        return value

    def calculate_total(self):
        self.total_amount = self.calculated_total_amount

# OrderItem Model
class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    order = relationship('Order', back_populates='order_items')
    product = relationship('Product', back_populates='order_items')

    __table_args__ = (
        Index('ix_orderitem_order_id', 'order_id'),
        Index('ix_orderitem_product_id', 'product_id'),
    )

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"

    def __str__(self):
        return self.__repr__()

    @validates('quantity')
    def validate_quantity(self, key, value):
        assert value > 0, "Quantity must be positive"
        return value
