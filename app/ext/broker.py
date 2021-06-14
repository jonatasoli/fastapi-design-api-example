import aiormq
from config import settings


async def create_broker_connection():
    broker_url = \
        f'amqp://{settings.BROKER_USER}:{settings.BROKER_PASS}@' + \
        f'{settings.BROKER_SERVER}:{settings.BROKER_PORT}/{settings.BROKER_VHOST}'
    connection = await aiormq.connect(broker_url)

    return connection
