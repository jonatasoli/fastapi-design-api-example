from pydantic_jsonapi import JsonApiModel
from pydantic import BaseModel, validator, ValidationError
from decimal import Decimal
from datetime import datetime


class orderBase(BaseModel):
    product_name: str
    total_amount: int


class orderCreate(orderBase):
    status: str


    class Config:
        orm_mode = True


class orderCreateResponse(orderCreate):
    id: int


    class Config:
        orm_mode = True

order_create_request, order_create_response = JsonApiModel('order_create_response', orderCreateResponse)
#response validation
response = {
    'data': {
        'id': '123',
        'type': 'order_create_response',
        'attributes': {
            'id': 1,
            'product_name': 'abcABC',
            'total_amount': 1000,
            'status': 'Waiting Payment',
        },
    },
    'links': {
        'self': '/api/order/123',
        'update': '/api/order/123',
        'cancel': '/api/order/123',
        'payment': '/api/payment/123',
    }
}
order_create_response(**response)


class orderUpdate(orderBase):
    ...


class orderUpdateResponse(orderBase):
    status: str
    id: int

    class Config:
        orm_mode = True

class orderGetResponse(orderBase):
    id: int
    status: str

    class Config:
        orm_mode = True

class orderListResponse(orderBase):
    ...
