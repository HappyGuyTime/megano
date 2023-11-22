from typing import Any, Optional

from django.core.management import BaseCommand

from products.models import Category


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """Custom management command to populate the database with categories and subcategories."""
        if Category.objects.exists():
            self.stdout.write(
                self.style.SUCCESS("Categories and subcategories already exist in the database.")
            )
            return

        categories_data = [
            {
                "title": "Electronics",
                "subcategory_titles": ["Phones", "Laptops"],
            },
            {"title": "Clothing", "subcategory_titles": ["T-shirts", "Jeans"]},
        ]

        for category_data in categories_data:
            parent_category = Category.objects.create(title=category_data["title"])
            subcategory_titles = category_data["subcategory_titles"]

            for subcategory_title in subcategory_titles:
                Category.objects.create(title=subcategory_title, category=parent_category)

        return (
            "Categories and subcategories have been successfully added to the database."
        )
