from django.db import models

from products.models import Product
from profiles.models import Profile


class Order(models.Model):
    """Model representing an order placed by a user."""

    createdAt = models.DateTimeField(auto_now_add=True)
    deliveryType = models.CharField(max_length=20, default="ordinary")
    paymentType = models.CharField(max_length=20, default="online")
    totalCost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default="processing")
    city = models.CharField(max_length=255, null=False, blank=True)
    address = models.CharField(max_length=255, null=False, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="orders")

    class Meta:
        db_table = "orders"

    def __str__(self):
        """String representation of the order."""
        return f"Order #{self.pk}"


class OrderProduct(models.Model):
    """Model representing a product in an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_products"
    )
    count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "orders_order_products"

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ) -> None:
        """Custom save method for OrderProduct to check product stock availability before saving."""
        product = self.product
        if product.count < self.count:
            raise Exception(f"Not enough stock for product {product.pk}.")
        super().save(force_insert, force_update, using, update_fields)
