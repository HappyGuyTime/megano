from typing import Any, Optional

from django.core.management import BaseCommand

from products.models import Tag


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """Custom management command to create predefined tags."""
        if Tag.objects.exists():
            self.stdout.write(
                self.style.SUCCESS("Predefined tags already exist in the database.")
            )
            return

        data = [
            "Electronics",
            "Clothing",
            "Home",
            "Music",
            "Movies",
        ]
        tags = [Tag(name=tag) for tag in data]
        Tag.objects.bulk_create(tags)

        return "Predefined tags have been created."
