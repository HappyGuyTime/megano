from typing import Any, Optional

from django.core.management import BaseCommand

from products.models import Specification


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """Custom management command to create predefined product specifications."""
        if Specification.objects.exists():
            self.stdout.write(
                self.style.SUCCESS("Predefined product specifications already exist in the database.")
            )
            return

        data = {
            "Dimensions": ("530x520 cm", "1530x1520 cm"),
            "Weight": ("1.3 kg", "300 g"),
            "Color": (
                "Red",
                "Black",
                "White",
            ),
            "Material": (
                "Steel",
                "Cotton",
            ),
            "Power": ("100 W", "150 W"),
        }

        specifications = [
            Specification(name=name, value=value)
            for name, values in data.items()
            for value in values
        ]
        Specification.objects.bulk_create(specifications)

        return "Predefined product specifications have been created."
