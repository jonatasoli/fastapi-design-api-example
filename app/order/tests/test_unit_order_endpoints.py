from fastapi import status
from datetime import datetime
from main import create_app
import json
import pytest

from order.api.endpoints import create_order
from order.service.business_rules import Order
from order.domains.order import orderBase, orderCreateResponse,\
    orderGetResponse, orderUpdateResponse

HEADERS = {"Content-Type": "application/json"}
 

def override_order():
    return orderCreateResponse(
        id=1,
        product_name="Latte",
        payment_status="Paid",
        total_amount=1000,
)
response_create = orderCreateResponse(
        id=1,
        product_name="Latte",
        payment_status="Paid",
        total_amount=1000,
)

def test_create_order(client, mocker):
    """Must return 201"""
    mocker.patch(
        "order.service.business_rules.Order.create",
        return_value=response_create
    )
    # order = Order()
    # mocker.patch.object(order, 'create')
    # order.create.return_value = [response_create]
    # create_app().dependency_overrides[Order.create] = lambda: order.create
    data = orderBase(product_name="Latte", payment_status="Created", total_amount=1000)
    response = client.post("/api/order", headers=HEADERS, json=data.dict())
    assert response.status_code == status.HTTP_201_CREATED
    import ipdb; ipdb.set_trace()
    # assert response.json() == json.loads(response_message.json())


def test_update_order_status(client, mocker):
    """Must return 200"""
    ...



def test_delete_order(client, mocker):
    """Must return 204"""
    ...


def test_get_order_current_status(client, mocker):
    """Must return 200"""
    ...


def test_process_order_payment(client, mocker):
    """Must return 204"""
    ...


def test_receipt_order(client, mocker):
    """Must return 200"""
    ...
