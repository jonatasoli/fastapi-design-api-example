from fastapi import APIRouter, status, Depends, HTTPException
from loguru import logger

from order.schemas.schemas_order import orderModelBase, messageBaseResponse
from order.services.services_order import OrderService

order_router = APIRouter()


# @order_router.post(
#     "/orders",
#     response_model=messageBaseResponse,
#     status_code=status.HTTP_201_CREATED
# )
# async def add_ordermodel(
#     data: orderModelBase,
#     order: OrderService = Depends()
# ):
#     try:
#         return await order.add_ordermodel(data)
#     except Exception as e:
#         logger.error(f"Error return endpoint {e.detail}")
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Error to proccess this request.\n{e.detail}"
#         )
