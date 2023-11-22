from django.db import transaction
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders import serializers, services
from orders.models import Order
from products.services import delete_basket


class OrderMixin:
    """Mixin for common functionality of Order API."""

    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "id"

    def get_object(self):
        """Get the order object or return a 404 error if the object is not found."""
        return get_object_or_404(Order, pk=self.kwargs.get(self.lookup_url_kwarg))


class OrderListCreateApiView(OrderMixin, generics.ListCreateAPIView):
    """API for creating and retrieving a list of orders."""

    serializer_class = serializers.OrderSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs) -> Response:
        """Create a new order and return its ID or validation errors."""
        order_products_data = services.get_order_products_data(request.data)
        order_serializer = self.get_serializer(data={"profile": request.user.profile.pk})
        order_product_serializer = serializers.OrderProductSerializer(
            data=order_products_data, many=True
        )

        with transaction.atomic():
            if order_serializer.is_valid() and order_product_serializer.is_valid():
                order = order_serializer.save()
                order_product_serializer.save(order=order)
                services.change_total_cost(order)
                delete_basket(request=request)
                return Response({"orderId": order.id}, status=status.HTTP_201_CREATED)

        if order_serializer.errors:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            order_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def get_queryset(self) -> QuerySet:
        """Return the queryset of orders for the user, sorted by creation date."""
        return Order.objects.filter(profile=self.request.user.profile).order_by(
            "createdAt"
        )


class OrderApiView(OrderMixin, generics.RetrieveUpdateAPIView):
    """API for retrieving and updating an order."""

    def post(self, request, *args, **kwargs) -> Response:
        """Handle a POST request to update the order and return the order's ID."""
        services.check_and_update_express_delivery(order_data=request.data)
        response = self.partial_update(request, *args, **kwargs)
        return Response({"orderId": response.data["id"]}, status=status.HTTP_200_OK)


class OrderPaymentApiView(OrderMixin, generics.UpdateAPIView):
    """API for updating payment information of an order."""

    def post(self, request, *args, **kwargs) -> Response:
        """Handle a POST request to update payment information and return the response status."""
        payment_serializer = serializers.PaymentSerializer(data=request.data)

        if payment_serializer.is_valid():
            request.data["status"] = "accepted"
            self.partial_update(request, *args, **kwargs)
            return Response(status=status.HTTP_200_OK)

        return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
