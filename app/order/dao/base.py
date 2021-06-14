from abc import ABCMeta
from typing import Any, Generic, Type, TypeVar, List

from fastapi.encoders import jsonable_encoder
from loguru import logger
from pydantic import BaseModel, parse_obj_as
from sqlalchemy.exc import DataError, DatabaseError, DisconnectionError, IntegrityError
from sqlalchemy.sql.expression import select, text

from ext.base_class import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType], metaclass=ABCMeta
):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update (CRU).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def obj_in_to_db_obj(self, obj_in: Any):
        obj_in_data = jsonable_encoder(obj_in)
        return self.model(**obj_in_data)

    def obj_in_to_db_obj_attrs(self, obj_in: Any, db_obj: Any):
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        return db_obj

    async def list(self, query: Any = None, order_by: Any = None):
        try:
            async with self.Meta.session() as db:
                full_query = select(self.model)
                if query is not None:
                    if not isinstance(query, list):
                        query = [query]
                    full_query = full_query.filter(*query)

                if order_by is not None:
                    full_query = full_query.order_by(text(order_by))

                smtm = await db.execute(full_query)

                items = smtm.scalars().all()
                return parse_obj_as(List[self.Meta.response_list_type], items)

        except (DataError, DatabaseError, DisconnectionError, IntegrityError) as err:
            logger.error(f"SQLAlchemy error {err}")
        except Exception as e:
            logger.error(f"Error in dao {e}")
            raise e

    async def _get_query(self, query: Any):
        try:
            async with self.Meta.session() as db:
                if not isinstance(query, list):
                    query = [query]
                smtm = await db.execute(select(self.model).filter(*query))
                return smtm.scalars().first()
        except (DataError, DatabaseError, DisconnectionError, IntegrityError) as err:
            logger.error(f"SQLAlchemy error {err}")
        except Exception as e:
            logger.error(f"Error in dao {e}")
            raise e

    async def _get(self, obj_id: Any):
        try:
            query = self.model.id == obj_id
            return await self._get_query(query)

        except (DataError, DatabaseError, DisconnectionError, IntegrityError) as err:
            logger.error(f"SQLAlchemy error {err}")
        except Exception as e:
            logger.error(f"Error in dao {e}")
            raise e

    async def get(self, obj_id: Any):
        try:
            db_obj = await self._get(obj_id)
            response = None
            if db_obj:
                response = self.Meta.response_get_type.from_orm(db_obj)
            return response

        except (DataError, DatabaseError, DisconnectionError, IntegrityError) as err:
            logger.error(f"SQLAlchemy error {err}")
        except Exception as e:
            logger.error(f"Error in dao {e}")
            raise e

    async def get_query(self, query: Any):
        try:
            db_obj = await self._get_query(query)
            response = None
            if db_obj:
                response = self.Meta.response_get_type.from_orm(db_obj)
            return response

        except (DataError, DatabaseError, DisconnectionError, IntegrityError) as err:
            logger.error(f"SQLAlchemy error {err}")
        except Exception as e:
            logger.error(f"Error in dao {e}")
            raise e

    async def update_or_create(self, query: Any, obj_in: CreateSchemaType) -> ModelType:
        result = await self.get_query(query)

        if not result:
            result = await self.create(obj_in)
            created = True

        else:
            result = await self.update(result.id, obj_in)
            created = False

        return result, created

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        try:
            data_db = self.obj_in_to_db_obj(obj_in=obj_in)
            async with self.Meta.session() as db:
                db.add(data_db)
                await db.commit()
                response = self.Meta.response_create_type.from_orm(data_db)

            return response
        except (DataError, DatabaseError, DisconnectionError, IntegrityError) as err:
            logger.error(f"SQLAlchemy error {err}")
        except Exception as e:
            logger.error(f"Error in dao {e}")
            raise e

    async def update(self, obj_id: Any, obj_in: UpdateSchemaType) -> ModelType:
        try:
            db_obj = await self._get(obj_id)
            response = None
            if db_obj:
                db_obj = self.obj_in_to_db_obj_attrs(obj_in, db_obj)
                async with self.Meta.session() as db:
                    db.add(db_obj)
                    await db.commit()
                    response = self.Meta.response_update_type.from_orm(db_obj)
            return response
        except (DataError, DatabaseError, DisconnectionError, IntegrityError) as err:
            logger.error(f"SQLAlchemy error {err}")
        except Exception as e:
            logger.error(f"Error in dao {e}")
            raise e
