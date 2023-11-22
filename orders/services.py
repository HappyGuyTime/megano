from typing import Dict, List

from django.db.models import Prefetch

from products.models import ProductSale
from products.services import change_product_count, get_total_price_product


def change_total_cost(order) -> None:
    """Calculate and update the total cost of an order."""
    product_sale_prefetch = Prefetch("product__sale", queryset=ProductSale.objects.all())
    order_products = (
        order.products.select_related("product")
        .prefetch_related(product_sale_prefetch)
        .all()
    )
    total_cost = 0

    for order_product in order_products:
        product = order_product.product
        change_product_count(product, order_product.count)
        total_cost += get_total_price_product(product, order_product.count)

    order.totalCost = total_cost
    order.save()


def check_and_update_express_delivery(order_data) -> None:
    """Check and update your order total if express shipping is selected."""
    express_delivery_price = 5
    if order_data.get("deliveryType") == "express":
        order_data["totalCost"] = express_delivery_price + float(order_data["totalCost"])


def get_order_products_data(order_products_data) -> List[Dict]:
    """Converts the list of order products and their quantity"""
    return [
        {
            "product": order_product_data.get("id"),
            "count": order_product_data.get("count"),
        }
        for order_product_data in order_products_data
    ]
