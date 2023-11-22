from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Sequential launch of all commands for creating data in the database"

    def handle(self, *args, **options):
        """Execute a sequence of predefined commands to create data in the database."""
        
        create_commands = [
            "create_categories",
            "create_specifications",
            "create_tags",
            "create_products",
            "create_reviews_for_products",
            "create_sale_products",
        ]

        for command_name in create_commands:
            call_command(command_name)

        self.stdout.write(self.style.SUCCESS("All commands were completed successfully."))
