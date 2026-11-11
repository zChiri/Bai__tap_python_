from sqlalchemy.orm import Session
from models.order import Order
from schemas.schemas import OrderCreate
from typing import Optional

def create_order(db:Session, order:OrderCreate) -> Optional[Order]:
    db_order = Order(item_name = order.item_name, total_price = order.total_price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db:Session, skip:int = 0, limit: int = 100) -> list[Order]:
    return db.query(Order).offset(skip).limit(limit).all()

def get_order(db:Session, order_id:int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()

def update_order(db:Session, order_id:int, order_update: OrderCreate) -> Optional[Order]:
    db_order = get_orders(db, order_id)
    if not db_order:
        return None
    db_order.item_name = order_update.item_name
    db_order.total_price = order_update.total_price
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db:Session, order_id:int) -> Optional[Order]:
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    db.delete(db_order)
    db.commit()
    return db_order