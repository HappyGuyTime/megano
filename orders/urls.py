from django.urls import path

from orders.views import (OrderApiView, OrderListCreateApiView,
                          OrderPaymentApiView)

app_name = "orders"


urlpatterns = [
    path("orders/", OrderListCreateApiView.as_view(), name="orders"),
    path("orders/<int:id>/", OrderApiView.as_view(), name="order_view"),
    path("payment/<int:id>/", OrderPaymentApiView.as_view(), name="payment"),
]
