from pydantic import BaseModel, Field

class OrderCreate(BaseModel):
    item_name: str = Field(..., min_length=3, max_length=200)
    total_price: int = Field(..., ge=0)

class OrderRead(OrderCreate):
    id: int 
    is_paid: bool
    class Config:
        from_attributes = True