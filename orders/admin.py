from django.contrib import admin

from orders.models import Order, OrderProduct
from orders.services import change_total_cost


class OrderProductInline(admin.TabularInline):
    """Inline for displaying order products within the OrderAdmin in the Django admin interface."""

    model = OrderProduct
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for the Order model."""

    inlines = (OrderProductInline,)
    list_display = (
        "createdAt",
        "totalCost",
        "status",
    )
    list_filter = (
        "status",
        "deliveryType",
        "paymentType",
    )
    readonly_fields = ("createdAt",)
    date_hierarchy = "createdAt"

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "createdAt",
                    "totalCost",
                    "status",
                    "deliveryType",
                    "paymentType",
                )
            },
        ),
        ("Shipping Information", {"fields": ("city", "address")}),
        ("Profile", {"fields": ("profile",)}),
    )

    def save_related(self, request, form, formsets, change) -> None:
        """Custom method to update the total cost of the order after saving related objects."""
        super().save_related(request, form, formsets, change)
        change_total_cost(form.instance)
