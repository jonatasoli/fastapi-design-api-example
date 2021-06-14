from order.models.models_order import Order
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings


def get_session():
    DBSession = sessionmaker(expire_on_commit=False, class_=AsyncSession)
    DBSession.configure(binds={Order: get_engine_main()})
    return DBSession()


def get_engine_main():
    """'postgresql://scott:tiger@localhost:5432/mydatabase'"""
    return create_async_engine(
        settings.DB_DSN_MAIN,
        echo=True,
    )
