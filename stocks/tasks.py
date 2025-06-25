from time import sleep
from celery import shared_task
from stocks.models import Stock
import random
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def get_stock_price(self, stock_name: str, num_of_digits: int) -> int:
    """
    Gera um preço aleatório para uma ação após um atraso de 60 segundos.
    
    Args:
        stock_name (str): Nome da ação
        num_of_digits (int): Número de dígitos no preço
        
    Returns:
        int: O preço gerado
    """
    task_id = self.request.id
    logger.info(f"Iniciando tarefa {task_id} para ação {stock_name}")
    
    # Simulando processamento demorado
    sleep(10)

    # Gerando preço aleatório
    num_in_text = ""
    for _ in range(num_of_digits):
        num_in_text += str(random.randint(0, 9))

    price = int(num_in_text)
    
    # Salvando no banco de dados
    Stock.objects.create(
        name=stock_name,
        price=price,
    )
    
    logger.info(f"Tarefa {task_id} concluída. Preço da ação {stock_name}: {price}")
    return price
