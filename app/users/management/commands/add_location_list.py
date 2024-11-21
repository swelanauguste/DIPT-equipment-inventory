import json

from django.core.management.base import BaseCommand

from ...models import Location


class Command(BaseCommand):
    help = "Load location data from JSON into the Location model."

    def handle(self, *args, **kwargs):
        # Load the JSON data
        with open("./static/docs/locations.json", "r") as file:
            data = json.load(file)

        added_count = 0
        skipped_count = 0

        for entry in data:
            fields = entry["fields"]
            name = str(fields["name"]).lower().strip()

            # Check if a location with the same name already exists
            if Location.objects.filter(name=name).exists():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Skipped: location'{name}' already exists.")
                )
                continue

            # Create or update the Location instance
            location = Location.objects.create(
                pk=entry["pk"],
                name=name,
            )
            added_count += 1

            # Log output
            self.stdout.write(self.style.SUCCESS(f"Added location: {name}"))

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {added_count} added, {skipped_count} skipped."
            )
        )
