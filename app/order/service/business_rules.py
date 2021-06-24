from fastapi import status, HTTPException

from order.adapters.orm_adapter import ordermodel


class Order:
    async def create(self, data):
        return await ordermodel.create(obj_in=data)

    async def update_status_waiting_payment(self, id):
        _order = await ordermodel.get(id)
        if not hasattr(_order, "payment_status") or _order.payment_status != "Waiting Payment":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update payment status is not permitted"
            )
        _order.payment_status = "paid"
        return await ordermodel.update(obj_id=id, obj_in=_order)

    async def cancel(self, id):
        _order = await ordermodel.get(id)
        if not hasattr(_order, "payment_status") or _order.payment_status != "Waiting Payment":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update payment status is not permitted"
            )
        _order.payment_status = "Cancelled"
        return await ordermodel.update(obj_id=id, obj_in=_order)

    async def status(self, id):
        _order = await ordermodel.get(id)
        if not hasattr(_order, "payment_status") or _order.payment_status != "Waiting Payment":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update payment status is not permitted"
            )
        return _order


class Payment:
    async def process(self, id):
        _order = await ordermodel.get(id)
        if not hasattr(_order, "payment_status") or _order.payment_status != "Waiting Payment":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update payment status is not permitted"
            )
        _order.payment_status = "Paid"
        return await ordermodel.update(obj_id=id, obj_in=_order)


class Receipt:
    async def delivery(self, id):
        _order = await ordermodel.get(id)
        if not hasattr(_order, "payment_status") or _order.payment_status != "Waiting Payment":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update payment status is not permitted"
            )
        _order.payment_status = "Delivery"
        return await ordermodel.update(obj_id=id, obj_in=_order)
