from fastapi import status
from datetime import datetime
import json
import pytest

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

def test_create_order(client, mocker):
    """Must return 201"""
    # mocker.patch(
    #     "order.domains.model.Order.create",
    #     return_value=response_message
    # )
    data = orderBase(product_name="Latte", payment_status="Created", total_amount=1000)
    response = client.post("/orders", headers=HEADERS, json=data.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == json.loads(response_message.json())


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
