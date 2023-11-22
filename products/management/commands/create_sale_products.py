from random import randint
from typing import Any, Optional

from django.core.management import BaseCommand

from products.models import Product, ProductSale


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """Custom management command to create random product sales."""
        if ProductSale.objects.exists():
            self.stdout.write(
                self.style.SUCCESS("Product sales already exist in the database.")
            )
            return
        
        products_sale = []
        unique_products = list(Product.objects.all())
        product_count = len(unique_products)

        for _ in range(25):
            if product_count > 0:
                product_index = randint(0, product_count - 1)
                product = unique_products.pop(product_index)
                product_count -= 1

                products_sale.append(
                    ProductSale(
                        product=product,
                        salePrice=product.price / 2,
                        dateFrom="11-08",
                        dateTo="11-21",
                    )
                )

        ProductSale.objects.bulk_create(products_sale)

        return "Random product sales have been created."
