from config import settings

from order.schemas.schemas_user import userBase
from ext.fetcher import fetcher


async def get_user(user_id):
    data = await fetcher(
        base_url=settings.BASE_URL_USER,
        method="GET",
        query=f"users/{user_id}"
    )
    return userBase(
        user_id=data["id"],
        firstName=data["firstName"],
        lastName=data["lastName"],
        customer_fullname=data["firstName"] + data["lastName"]
    )
