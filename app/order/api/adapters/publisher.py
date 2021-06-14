from loguru import logger
from tenacity import retry, stop_after_delay, wait_random_exponential
from config import settings

from ext.broker import create_broker_connection


@retry(
    reraise=True,
    stop=stop_after_delay(settings.BROKER_STOP_DELAY),
    wait=wait_random_exponential(multiplier=1, max=settings.BROKER_MAX_DELAY),
)
async def publish_queue(
    broker_queue,
    broker_exchange,
    body_queue,
    exchange_type="direct"
):

    try:
        connection = await create_broker_connection()
        channel = await connection.channel()
        await channel.exchange_declare(
            exchange=broker_exchange, exchange_type=exchange_type
        )

        _routing_key = broker_queue
        response = await channel.basic_publish(
            body=body_queue,
            routing_key=_routing_key,
            exchange=broker_exchange,
        )

        await connection.close()
        return response
    except Exception as e:
        logger.error(f"Error in publisher adapter.\n{e}")
        raise e
