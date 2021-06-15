from .base import CRUDBase

from ext.database import get_session
from order.schemas.schemas_order import (
    orderCreateResponse,
    orderUpdateResponse,
    orderGetResponse,
    orderListResponse,
    orderBase,
    orderCreate,
    orderUpdate,
)


class CRUDorderModel(
    CRUDBase[
        orderBase,
        orderCreate,
        orderUpdate,
    ]
):
    class Meta:
        response_create_type = orderCreateResponse
        response_update_type = orderUpdateResponse
        response_get_type = orderGetResponse
        response_list_type = orderListResponse
        session = get_session
