from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    orders = relationship("Orders", back_populates="customer")