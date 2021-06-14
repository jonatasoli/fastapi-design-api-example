import httpx
from httpx import TimeoutException, HTTPStatusError, RequestError
from fastapi import status, HTTPException
from config import settings
from loguru import logger

from tenacity import retry, stop_after_delay, wait_fixed


@retry(
    reraise=True,
    stop=stop_after_delay(settings.MICROSERVICE_MAX_SECONDS_RETRY),
    wait=wait_fixed(settings.MICROSERVICE_MAX_SECONDS_WAIT)
)
async def fetcher(base_url, method, query):
    try:
        async with httpx.AsyncClient(
            base_url=base_url,
            timeout=settings.MICROSERVICES_TIMEOUT
        ) as client:
            response = None
            if method == "GET":
                response = await client.get(query)

            if not response:
                raise RequestError("The request did not generate a response")

            response.raise_for_status()
            data = response.json()

            if not data:
                raise ValueError(f"The {query} not have data")

            return data

    except TimeoutException as te:
        logger.error(te)
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Error to try get request.\n {te.request.url}"
        )
    except HTTPStatusError as ne:
        logger.error(ne)
        raise HTTPException(
            status_code=ne.response.status_code,
            detail=f"Internal Error\n {ne}"
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error generic\n {e}"
        )
