from enum import Enum
from fastapi import status, HTTPException

from order.adapters.orm_adapter import ordermodel


class Order:
    async def create(self, data):
        return await ordermodel.create(obj_in=data)

    async def update(self, id, data):
        _order = await ordermodel.get(id)
        if not hasattr(_order, "status")\
            or _order.status != OrderStatus.WAITING.value:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Current Status in payment status is not permitted"
            )

        _order.product_name = data.product_name
        _order.total_amount = data.total_amount
        return await ordermodel.update(obj_id=id, obj_in=_order)

    async def cancel(self, id):
        _order = await ordermodel.get(id)
        if not hasattr(_order, "status")\
            or _order.status != OrderStatus.WAITING.value:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update payment status is not permitted"
            )

        _order.status = OrderStatus.CANCELLED.value

        return await ordermodel.update(obj_id=id, obj_in=_order)

    async def status(self, id):
        return await ordermodel.get(id)


class Payment:
    async def process(self, id):
        _order = await ordermodel.get(id)
        if not hasattr(_order, "status")\
            or _order.status != OrderStatus.WAITING.value:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update payment status is not permitted"
            )
        _order.status = OrderStatus.PAID.value
        return await ordermodel.update(obj_id=id, obj_in=_order)


class Receipt:
    async def delivery(self, id):
        _order = await ordermodel.get(id)
        if not hasattr(_order, "status")\
            or _order.status != OrderStatus.READY.value:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update payment status is not permitted"
            )
        _order.status = OrderStatus.DELIVERY.value
        return await ordermodel.update(obj_id=id, obj_in=_order)


class OrderStatus(Enum):
    WAITING="Waiting Payment"
    CANCELLED="Canceled"
    PAID="Paid"
    READY="Ready"
    DELIVERY="Delivery"
