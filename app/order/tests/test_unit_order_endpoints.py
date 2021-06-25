from fastapi import status, HTTPException
from datetime import datetime
from main import create_app
import json
import pytest

from order.api.endpoints import create_order
from order.service.business_rules import Order
from order.domains.order import orderBase, orderCreateResponse,\
    orderGetResponse, orderUpdateResponse

HEADERS = {"Content-Type": "application/json"}


response_create = orderCreateResponse(
        id=1,
        product_name="Latte",
        payment_status="Waiting Payment",
        status="Created",
        total_amount=1000,
)
response_update = orderUpdateResponse(
        id=42,
        product_name="Latte",
        payment_status="Paid",
        status="Created",
        total_amount=1000,
)
response_status = orderGetResponse(
        id=42,
        product_name="Latte",
        payment_status="Paid",
        status="Delivery",
        total_amount=1000,
)


def test_error_route(client):
    """Must return 404, route without serve name"""
    data = orderBase(product_name="Latte", total_amount=1000)
    response = client.post("/order", headers=HEADERS, json=data.dict())
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_order(client, mocker):
    """Must return 201"""
    mocker.patch(
        "order.service.business_rules.Order.create",
        return_value=response_create
    )
    data = orderBase(product_name="Latte", total_amount=1000)
    response = client.post("/api/order", headers=HEADERS, json=data.dict())
    assert response.status_code == status.HTTP_201_CREATED


def test_create_order_conflict(client, mocker):
    """Must return 409 - conflict with payment state"""
    mocker.patch(
        "order.service.business_rules.Order.create",
        side_effect=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sended payment status not permitted"
        )
    )
    data = orderBase(product_name="Latte", total_amount=1000)
    response = client.post("/api/order", headers=HEADERS, json=data.dict())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_error_data_order(client):
    """Must return 422, error in structure data"""
    data = dict(product_name="Latte")
    response = client.post("/api/order", headers=HEADERS, json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_order_status(client, mocker):
    """Must return 200"""
    mocker.patch(
        "order.service.business_rules.Order.update_status_waiting_payment",
        return_value=response_update
    )
    response = client.put("/api/order/42", headers=HEADERS, )
    assert response.status_code == status.HTTP_200_OK


def test_update_order_status_conflict(client, mocker):
    """Must return 409"""
    mocker.patch(
        "order.service.business_rules.Order.update_status_waiting_payment",
        side_effect=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sended payment status not permitted"
        )
    )
    response = client.put("/api/order/42", headers=HEADERS, )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_delete_order(client, mocker):
    """Must return 204"""
    mocker.patch(
        "order.service.business_rules.Order.cancel",
        return_value=response_update
    )
    response = client.delete("/api/order/42", headers=HEADERS)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_order_coflict(client, mocker):
    """Must return 409"""
    mocker.patch(
        "order.service.business_rules.Order.cancel",
        side_effect=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sended payment status not permitted"
        )
    )
    response = client.delete("/api/order/42", headers=HEADERS)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_get_order_current_status(client, mocker):
    """Must return 200"""
    mocker.patch(
        "order.service.business_rules.Order.status",
        return_value=response_update
    )
    response = client.get("/api/order/42", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK


def test_process_order_payment(client, mocker):
    """Must return 204"""
    mocker.patch(
        "order.service.business_rules.Payment.process",
        return_value=response_status
    )
    response = client.put("/api/payment/42", headers=HEADERS)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_process_order_payment_conflict(client, mocker):
    """Must return 409"""
    mocker.patch(
        "order.service.business_rules.Payment.process",
        side_effect=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sended payment status not permitted"
        )
    )
    response = client.put("/api/payment/42", headers=HEADERS)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_receipt_order(client, mocker):
    """Must return 200"""
    mocker.patch(
        "order.service.business_rules.Receipt.delivery",
        return_value=response_status
    )
    response = client.delete("/api/receipt/42", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK


def test_receipt_order_conflict(client, mocker):
    """Must return 409"""
    mocker.patch(
        "order.service.business_rules.Receipt.delivery",
        side_effect=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sended payment status not permitted"
        )
    )
    response = client.delete("/api/receipt/42", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
