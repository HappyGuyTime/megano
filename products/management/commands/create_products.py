from random import choice
from typing import Any, Optional

from django.core.management import BaseCommand

from products.models import Category, Product, Specification, Tag


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """Custom management command to populate the database with sample products."""
        if Product.objects.exists():
            self.stdout.write(
                self.style.SUCCESS("Sample products already exist in the database.")
            )
            return
        
        data = {
            "Phones": {
                "price_multiplier": 599.99,
                "title_prefix": "iPhone",
                "description": "A high-end smartphone.",
                "count_multiplier": 10,
                "tags": [1, 3, 4, 5],
                "specifications": [1, 4, 5, 8, 10],
            },
            "Laptops": {
                "price_multiplier": 1599.99,
                "title_prefix": "Laptop",
                "description": "A high-end laptop.",
                "count_multiplier": 10,
                "tags": [1, 4, 5],
                "specifications": [2, 3, 6, 8, 11],
            },
            "T-shirts": {
                "price_multiplier": 9.99,
                "title_prefix": "Basic T-shirt",
                "description": "A comfortable cotton T-shirt.",
                "count_multiplier": 10,
                "tags": [2, 3],
                "specifications": [7, 9],
            },
            "Jeans": {
                "price_multiplier": 19.99,
                "title_prefix": "Basic Jeans",
                "description": "A comfortable cotton Jeans.",
                "count_multiplier": 10,
                "tags": [2, 3],
                "specifications": [5, 9],
            },
        }

        categories = Category.objects.all()
        tags = Tag.objects.all()
        specifications = Specification.objects.all()

        for number in range(1, 11):
            for category_title, info in data.items():
                price = info["price_multiplier"] * number
                title = f'{info["title_prefix"]} {number}'
                description = info["description"]

                product = Product.objects.create(
                    price=price,
                    count=info["count_multiplier"] * number,
                    title=title,
                    description=description,
                    fullDescription=f"""The {title} features a Super Retina XDR display and A{4 + number} Bionic chip."""
                    if category_title == "Phones"
                    else f"The {title} features a Super Retina XDR display",
                    freeDelivery=choice([True, False]),
                    category=categories.get(title=category_title),
                )
                product.tags.set(tags.filter(id__in=info["tags"]))
                product.specifications.set(
                    specifications.filter(id__in=info["specifications"])
                )

        return "Sample products have been successfully added to the database."
