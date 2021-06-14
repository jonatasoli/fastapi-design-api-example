from config import settings

from order.schemas.schemas_product import productBase
from ext.fetcher import fetcher


async def get_product(product_code):
    data = await fetcher(
        base_url=settings.BASE_URL_PRODUCT,
        method="GET",
        query=f"products/{product_code}")
    return productBase(
        product_code=data["code"],
        product_name=data["name"],
        price = data["price"]
    )
