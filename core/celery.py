import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Criar instância do Celery
app = Celery('core')

# Configuração usando variáveis de ambiente
# Obter a URL do broker a partir de variáveis de ambiente ou usar o padrão
app.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//')
app.conf.result_backend = 'django-db'  # Usar o banco de dados Django como backend

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# this is used in order to make Celery use Django Environment
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    timezone='America/Sao_Paulo',
    task_routes={
        'stocks.tasks.*': {'queue': 'default'}
    },
)
# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self) -> None:
    print(f'Request: {self.request!r}')