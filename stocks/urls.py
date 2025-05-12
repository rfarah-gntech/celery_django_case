from django.urls import path
from .views import StockPriceView

urlpatterns = [
    path("stock/", StockPriceView.as_view(), name="get_stock_price")
]
