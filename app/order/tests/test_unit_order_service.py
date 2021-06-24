import pytest

from order.service.business_rules import Order
from order.domains.order import orderCreateResponse, orderUpdateResponse, orderGetResponse, orderBase
from order.service.business_rules import Order, Payment, Receipt

base_data = orderBase(
        product_name="Latte",
        payment_status="Created",
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
