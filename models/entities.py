from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    func
)

from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
class Table(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=True)

    orders = relationship("Order", back_populates="table")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey('tables.id'))
    timestamp = Column(DateTime, default=func.now())

    table = relationship("Table", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    price = Column(Float, nullable=False)
    
    order_items = relationship("OrderItem", back_populates="product")

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

