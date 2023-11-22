from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from orders.models import Order, OrderProduct
from products.serializers import ProductImageSerializer, TagSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    """Serializer for OrderProduct objects."""

    date = serializers.DateTimeField(source="product.date", read_only=True)
    price = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(
        source="product.category", read_only=True
    )
    title = serializers.CharField(source="product.title", read_only=True)
    description = serializers.CharField(source="product.description", read_only=True)
    freeDelivery = serializers.BooleanField(source="product.freeDelivery", read_only=True)
    images = ProductImageSerializer(source="product.images", many=True, read_only=True)
    tags = TagSerializer(source="product.tags", many=True, read_only=True)
    reviews = serializers.PrimaryKeyRelatedField(
        source="product.reviews", many=True, read_only=True
    )
    rating = serializers.DecimalField(
        source="product.rating", max_digits=2, decimal_places=1, read_only=True
    )

    class Meta:
        model = OrderProduct
        exclude = ("order",)
        extra_kwargs = {
            "product": {"write_only": True},
        }

    def get_price(self, obj) -> float:
        """
        Get the price of the associated product. If the product is on sale,
        return the sale price, otherwise, return the regular price.
        """
        product = obj.product
        if hasattr(product, "sale"):
            return product.sale.salePrice
        return product.price


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order objects."""

    fullName = serializers.CharField(source="profile.fullName", read_only=True)
    email = serializers.EmailField(source="profile.user.email", read_only=True)
    phone = serializers.CharField(source="profile.phone", read_only=True)
    products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {
            "profile": {"write_only": True},
        }


class PaymentSerializer(serializers.Serializer):
    """Serializer for Payment data."""

    number = serializers.CharField(max_length=16)
    name = serializers.CharField(max_length=128)
    month = serializers.CharField(max_length=2)
    year = serializers.CharField(max_length=4)
    code = serializers.CharField(max_length=3, min_length=3)

    def validate_number(self, value):
        """Validate the 'number' field to ensure it is a positive number."""
        if not value.isdigit():
            raise ValidationError("Make sure this field is a positive number.")
        return value

    def validate_code(self, value):
        """Validate the 'code' field to ensure it is a positive number."""
        if not value.isdigit():
            raise ValidationError("Make sure this field is a positive number.")
        return value

    def validate(self, data):
        """Validate the payment data, including the 'month' and 'year' fields to ensure they represent a valid date."""
        month = data.get("month")
        year = data.get("year")

        try:
            datetime(int(year), int(month), 1)
        except ValueError:
            raise ValidationError("Not a valid date.")
        return data
