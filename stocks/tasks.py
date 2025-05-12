from time import sleep
from celery import shared_task
from stocks.models import Stock
import random
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def get_stock_price(stock_name: str, num_of_digits: int) -> int:
    logger.info("🟡 Iniciando task get_stock_price")

    sleep(5)

    num_in_text = ""
    for _ in range(num_of_digits):
        num_in_text += str(random.randint(0, 9))

    price = int(num_in_text)

    Stock.objects.create(
        name=stock_name,
        price=price,
    )

    logger.info(f"✅ Task concluída — Inserido: {stock_name} com valor {price}")
    logger.info(f"📦 Banco em uso: {settings.DATABASES['default']}")

    return price
