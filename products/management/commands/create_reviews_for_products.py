import random
import string
from datetime import datetime
from typing import Any, Optional

from django.core.management import BaseCommand

from products.models import Product, Review
from products.services import change_product_rating


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """Custom management command to generate random reviews for existing products."""
        if Review.objects.exists():
            self.stdout.write(
                self.style.SUCCESS("Reviews for products already exist in the database.")
            )
            return

        products = Product.objects.all()
        for product in products:
            for _ in range(random.randint(1, 5)):
                author = "".join(random.choice(string.ascii_letters) for _ in range(5))
                Review.objects.create(
                    author=author,
                    email=f"{author}@example.com",
                    text="".join(random.choice(string.ascii_letters) for _ in range(20)),
                    rate=random.randint(1, 5),
                    date=datetime.now(),
                    product=product,
                )

            change_product_rating(
                reviews=Review.objects.filter(product=product),
                product=product,
            )

        return "Random reviews have been generated and product ratings have been updated."
