from sqlalchemy import Column, Integer, Boolean, DateTime, 
from sqlalchemy.orm import relationship
from database import Base

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(200), nullable=False)
    total_price = Column(Integer, nullable=False)
    is_paid = Column(Boolean, default=False)
    create_at = Column(DateTime, server_default= func.now())
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    customer = relationship('Customer', back_populates="order")