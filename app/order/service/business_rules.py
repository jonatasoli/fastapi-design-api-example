from fastapi import status


class Order:
    async def create(self,data):
        raise Exception(f"{data}")

    async def update_status_waiting_payment(id):
        ...

    async def cancel(id):
        ...

    async def status(id):
        ...


class Payment:
    async def process(id):
        ...


class Receipt:
    async def delivery(id):
        ...
