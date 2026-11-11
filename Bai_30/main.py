from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from schemas.schemas import OrderCreate, OrderRead
from database import Base, engine, get_db
from services.orders import get_order as go, get_orders as gos, create_order as co, update_order as uo, delete_order as do
from models.customer import Customer

Base.metadata.create_all(bind_engine)

app = FastAPI(title="Order Management API")

@app.post("/orders", response_model=OrderRead, status_code=201)
def create_order(order:OrderCreate, db:Session=Depends(get_db)):
    return co(db=db, order=order)

@app.get("/orders", response_model=List[OrderRead])
def get_orders(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    return gos(skip=skip, limit=limit, db=db)

@app.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id:int, db:Session = Depends(get_db)):
    return go(order_id=order_id, db=db)

@app.put("/orders/{order_id}", response_model=OrderRead)
def update_order(order_id:int, order_update = OrderCreate, db:Session = Depends(get_db)):
    db_order = uo(db=db, order_id=order_id, order_update= order_update)
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khong tim thay du lieu!")
    return db_order

@app.delete("/orders/{order_id}", response_model=OrderRead)
def delete_order(order_id:int, db:Session=Depends(get_db)):
    db_order = do(db=db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Khong  tim thay du lieu!")
    return db_order
