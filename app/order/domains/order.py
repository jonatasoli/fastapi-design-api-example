from pydantic import BaseModel, validator, ValidationError
from decimal import Decimal
from datetime import datetime


class orderBase(BaseModel):
    product_name: str
    total_amount: int


class orderCreate(orderBase):
    payment_status: str
    status: str


    class Config:
        orm_mode = True


class orderCreateResponse(orderCreate):
    id: int


    class Config:
        orm_mode = True


class orderUpdate(orderBase):
    payment_status: str
    status: str


class orderUpdateResponse(orderBase):
    payment_status: str
    status: str
    id: int


class orderGetResponse(orderBase):
    id: int
    payment_status: str
    status: str


class orderListResponse(orderBase):
    ...
