from ext.db.base_class import BaseModel
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.types import Numeric
from datetime import datetime


class Order(BaseModel):
    id = Column(Integer, primary_key=True)
