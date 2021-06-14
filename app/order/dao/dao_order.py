from .base import CRUDBase

from ext.database import get_session
from order.schemas.schemas_order import (
    orderModelCreateResponse,
    orderModelUpdateResponse,
    orderModelGetResponse,
    orderModelListResponse,
    orderModelBase,
    orderModelCreate,
    orderModelUpdate,
)


class CRUDorderModel(
    CRUDBase[
        orderModelBase,
        orderModelCreate,
        orderModelUpdate,
    ]
):
    class Meta:
        response_create_type = orderModelCreateResponse
        response_update_type = orderModelUpdateResponse
        response_get_type = orderModelGetResponse
        response_list_type = orderModelListResponse
        session = get_session
