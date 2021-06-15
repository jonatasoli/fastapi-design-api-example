from pydantic import BaseModel, validator, ValidationError
from decimal import Decimal
from datetime import datetime


class orderBase(BaseModel):
    product_name: str
    payment_status: str
    total_amount: int


class orderCreate(orderBase):


    class Config:
        orm_mode = True


class orderCreateResponse(orderCreate):
    id: int


    class Config:
        orm_mode = True


class orderUpdate(orderBase):
    ...


class orderUpdateResponse(orderBase):
    id: int


class orderGetResponse(orderBase):
    id: int


class orderListResponse(orderBase):
    ...
