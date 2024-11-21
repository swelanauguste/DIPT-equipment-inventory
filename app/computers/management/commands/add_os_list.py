import json

from django.core.management.base import BaseCommand

from ...models import OperatingSystem


class Command(BaseCommand):
    help = "Load os data from JSON into the OperatingSystem model."

    def handle(self, *args, **kwargs):
        # Load the JSON data
        with open("./static/docs/os.json", "r") as file:
            data = json.load(file)

        added_count = 0
        skipped_count = 0

        for entry in data:
            fields = entry["fields"]
            name = str(fields["name"]).lower().strip()

            # Check if a os with the same name already exists
            if OperatingSystem.objects.filter(name=name).exists():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Skipped: os'{name}' already exists.")
                )
                continue

            # Create or update the OperatingSystem instance
            os = OperatingSystem.objects.create(
                pk=entry["pk"],
                name=name,
            )
            added_count += 1

            # Log output
            self.stdout.write(self.style.SUCCESS(f"Added os: {name}"))

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {added_count} added, {skipped_count} skipped."
            )
        )
