from fastapi import status

from order.adapters.orm_adapter import ordermodel


class Order:
    async def create(self, data):
        return await ordermodel.create(obj_in=data)

    async def update_status_waiting_payment(self, id):
        ...

    async def cancel(self, id):
        ...

    async def status(self, id):
        ...


class Payment:
    async def process(self, id):
        ...


class Receipt:
    async def delivery(self, id):
        ...
