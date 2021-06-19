from fastapi import APIRouter, status, Depends, HTTPException
from loguru import logger

from order.domains.order import orderBase, orderCreateResponse,\
    orderGetResponse, orderUpdateResponse
from order.service.business_rules import Order, Payment, Receipt

order_router = APIRouter()


@order_router.post(
    "/order",
    response_model=orderCreateResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_order(
    data: orderBase,
    order: Order = Depends()
):
    """
    Create order
    """
    try:
        return await order.create(data)
    except Exception as e:
        logger.error(f"Error return endpoint {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error to proccess this request.\n{e.detail}"
        )


@order_router.put(
    "/order",
    response_model=orderUpdateResponse,
    status_code=status.HTTP_200_OK
)
async def update_status_waiting_payment(
    _id: int,
    order: Order = Depends()
):
    """
    Must update order if current status is "Waiting Payment"
    """
    try:
        return await order.update_waiting_status(_id)
    except Exception as e:
        logger.error(f"Error return endpoint {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error to proccess this request.\n{e.detail}"
        )


@order_router.delete(
    "/order",
    status_code=status.HTTP_204_NO_CONTENT
)
async def cancel_order(
    _id: int,
    order: Order = Depends()
):
    """
    Must cancel order if current status is "Waiting Payment"
    """
    try:
        await order.cancel(_id)
    except Exception as e:
        logger.error(f"Error return endpoint {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error to proccess this request.\n{e.detail}"
        )


@order_router.get(
    "/order",
    response_model=orderGetResponse,
    status_code=status.HTTP_200_OK
)
async def order_status(
    _id: int,
    order: Order = Depends()
):
    """
    Get order current status
    """
    try:
        return await order.status(data)
    except Exception as e:
        logger.error(f"Error return endpoint {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error to proccess this request.\n{e.detail}"
        )


@order_router.put(
    "/payment",
    status_code=status.HTTP_204_NO_CONTENT
)
async def process_payment(
    _id: int,
    payment: Payment = Depends()
):
    """
    Process payment if current status is "Waiting Payment"
    """
    try:
        await payment.process(data)
    except Exception as e:
        logger.error(f"Error return endpoint {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error to proccess this request.\n{e.detail}"
        )


@order_router.delete(
    "/receipt",
    response_model=orderGetResponse,
    status_code=status.HTTP_200_OK
)
async def receive_delivery(
    _id: int,
    receipt: Receipt = Depends()
):
    """
    Update order to "Receipt" status
    """
    try:
        return await receipt.delivery(data)
    except Exception as e:
        logger.error(f"Error return endpoint {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error to proccess this request.\n{e.detail}"
        )
