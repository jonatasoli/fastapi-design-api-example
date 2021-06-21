from fastapi import status


class Order:
    async def create(self, data):
        raise Exception(f"{data}")

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
