import json

from django.core.management.base import BaseCommand

from ...models import Maker


class Command(BaseCommand):
    help = "Load maker data from JSON into the Maker model."

    def handle(self, *args, **kwargs):
        # Load the JSON data
        with open("./static/docs/computers/maker_list.json", "r") as file:
            data = json.load(file)

        added_count = 0
        skipped_count = 0

        for entry in data:
            fields = entry["fields"]
            name = str(fields["name"]).lower().strip()

            # Check if a maker with the same name already exists
            if Maker.objects.filter(name=name).exists():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Skipped: maker'{name}' already exists.")
                )
                continue

            # Create or update the Maker instance
            maker = Maker.objects.create(
                pk=entry["pk"],
                name=name,
            )
            added_count += 1

            # Log output
            self.stdout.write(self.style.SUCCESS(f"Added maker: {name}"))

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {added_count} added, {skipped_count} skipped."
            )
        )
