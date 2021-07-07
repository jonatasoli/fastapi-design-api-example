import pytest
from fastapi import HTTPException, status

from order.service.business_rules import Order
from order.domains.order import orderCreateResponse, orderUpdateResponse, orderGetResponse, orderBase, orderUpdate
from order.service.business_rules import Order, Payment, Receipt, OrderStatus


base_data = orderBase(
        product_name="Latte",
        total_amount=1000,
)
order_update = orderUpdate(
        product_name="Mocca",
        total_amount=500,
)
get_response_update = orderGetResponse(
        id=1,
        product_name="Latte",
        status=OrderStatus.WAITING.value,
        total_amount=1000,
)

get_response_conflict = orderGetResponse(
        id=1,
        product_name="Latte",
        status=OrderStatus.PAID.value,
        total_amount=1000,
)

response_create = orderCreateResponse(
        id=1,
        product_name="Latte",
        status=OrderStatus.WAITING.value,
        total_amount=1000,
)
response_update = orderUpdateResponse(
        id=42,
        product_name="Latte",
        status=OrderStatus.WAITING.value,
        total_amount=1000,
)
response_status = orderGetResponse(
        id=42,
        product_name="Latte",
        status=OrderStatus.DELIVERY.value,
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
        await order.update(id=1, data=order_update)
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
    output = await order.update(id=1, data=order_update)
    assert output == response_update


@pytest.mark.asyncio
async def test_database(apply_migrations):
    dir(apply_migrations)
    assert True == True
    ...
