from config import settings
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from order.api.endpoints import order_router


order = FastAPI(
    title=settings.APP_NAME,
)


origins = [
    "localhost",
]

order.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

order.include_router(
    order_router, responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not found"}
    }
)
