from rest_framework import views, response, status
from stocks.models import Stock
from stocks.serializers import StockSerializer
from stocks.tasks import get_stock_price

class StockPriceView(views.APIView):

    def post(self, request):
        stock_name = request.data.get("stock_name")
        num_of_digits = int(request.data.get("num_of_digits"))

        get_stock_price.delay(stock_name, num_of_digits)

        return response.Response(
            data={
                "message": "Task has been sent successfully!"},
                status=status.HTTP_200_OK
        )
    
    def get(self, request):
        stocks = Stock.objects.all()

        return response.Response(
            data=StockSerializer(stocks, many=True).data,
            status=status.HTTP_200_OK,
        )