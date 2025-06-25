from rest_framework import views, response, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from stocks.models import Stock
from stocks.serializers import StockSerializer
from stocks.tasks import get_stock_price

class StockPriceView(views.APIView):
    
    @swagger_auto_schema(
        operation_description="Obtém uma lista de todos os preços de ações armazenados",
        responses={200: StockSerializer(many=True)}
    )
    def get(self, request):
        """
        Retorna todas as ações armazenadas no banco de dados.
        """
        stocks = Stock.objects.all()

        return response.Response(
            data=StockSerializer(stocks, many=True).data,
            status=status.HTTP_200_OK,
        )
    
    @swagger_auto_schema(
        operation_description="Inicia uma tarefa assíncrona para gerar um preço de ação",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['stock_name', 'num_of_digits'],
            properties={
                'stock_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nome da ação'),
                'num_of_digits': openapi.Schema(type=openapi.TYPE_INTEGER, description='Número de dígitos para o preço'),
            }
        ),
        responses={
            200: openapi.Response(
                description="Tarefa iniciada com sucesso",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'task_ids': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            description='Lista de IDs das tarefas para rastreamento'
                        ),
                    }
                )
            )
        }
    )
    def post(self, request):
        """
        Inicia uma tarefa assíncrona para gerar um preço de ação.
        A tarefa leva 60 segundos para ser concluída.
        """
        stock_name = request.data.get("stock_name")
        num_of_digits = int(request.data.get("num_of_digits"))
        
        # Envia múltiplas tarefas para teste (melhor visualização no RabbitMQ)
        task_ids = []
        for i in range(5):  # Reduzido para 5 tarefas para não sobrecarregar
            task = get_stock_price.delay(f"{stock_name}_{i}", num_of_digits)
            task_ids.append(task.id)
        
        return response.Response(
            data={
                "message": "5 tasks have been sent successfully!",
                "task_ids": task_ids  # Retorna lista de IDs das tarefas
            },
            status=status.HTTP_200_OK
        )