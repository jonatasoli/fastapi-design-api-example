from .dao_order import CRUDorderModel
from order.models.models_order import Order


ordermodel = CRUDorderModel(Order)
