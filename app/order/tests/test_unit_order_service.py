import pytest
from fastapi import HTTPException, status

from order.service.business_rules import Order
from order.domains.order import orderCreateResponse, orderUpdateResponse, orderGetResponse, orderBase
from order.service.business_rules import Order, Payment, Receipt


base_data = orderBase(
        product_name="Latte",
        payment_status="Created",
        total_amount=1000,
)
get_response_update = orderGetResponse(
        id=1,
        product_name="Latte",
        payment_status="Waiting Payment",
        total_amount=1000,
)

get_response_conflict = orderGetResponse(
        id=1,
        product_name="Latte",
        payment_status="Paid",
        total_amount=1000,
)

response_create = orderCreateResponse(
        id=1,
        product_name="Latte",
        payment_status="Waiting Payment",
        total_amount=1000,
)
response_update = orderUpdateResponse(
        id=42,
        product_name="Latte",
        payment_status="Paid",
        total_amount=1000,
)
response_status = orderGetResponse(
        id=42,
        product_name="Latte",
        payment_status="Deliveried",
        total_amount=1000,
)

@pytest.mark.asyncio
async def test_create_rule(mocker):
    mocker.patch(
        "order.adapters.orm_adapter.ordermodel.create",
        return_value=response_create
    )
    order = Order()
    output = await order.create(data=base_data)
    assert output == response_create


@pytest.mark.asyncio
async def test_update_payment_status_conflict(mocker):
    mocker.patch(
        "order.adapters.orm_adapter.ordermodel.update",
        return_value=response_update
    )
    mocker.patch(
        "order.adapters.orm_adapter.ordermodel.get",
        return_value=get_response_conflict
    )
    order = Order()
    with pytest.raises(HTTPException) as exc_info:
        await order.update_status_waiting_payment(id=1)
    assert exc_info.value.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_update_payment_status(mocker):
    mocker.patch(
        "order.adapters.orm_adapter.ordermodel.update",
        return_value=response_update
    )
    mocker.patch(
        "order.adapters.orm_adapter.ordermodel.get",
        return_value=get_response_update
    )
    order = Order()
    output = await order.update_status_waiting_payment(id=1)
    assert output == response_update
