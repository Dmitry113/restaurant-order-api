from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)  # новое поле

    orders = relationship("OrderDish", back_populates="dish")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    order_time = Column(DateTime, default=datetime.utcnow)  # изменено название поля
    status = Column(String, nullable=False, default="в обработке")  # новое поле со значением по умолчанию

    dishes = relationship("OrderDish", back_populates="order")


class OrderDish(Base):
    __tablename__ = "order_dishes"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="dishes")
    dish = relationship("Dish", back_populates="orders")
