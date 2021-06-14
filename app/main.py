from fastapi import FastAPI

from order import order
from ext.factory_logging import init_log


def create_app():
    try:
        init_log()
        app = FastAPI()
        app.mount("/", order)
        return app
    except Exception as e:
        raise e
