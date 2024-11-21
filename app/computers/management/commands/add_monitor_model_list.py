import json

from django.core.management.base import BaseCommand

from ...models import Maker, MonitorModel


class Command(BaseCommand):
    help = "Load monitor model data from JSON into the MonitorModel model."

    def handle(self, *args, **kwargs):
        # Load the JSON data
        with open("./static/docs/mm.json", "r") as file:
            data = json.load(file)

        added_count = 0
        skipped_count = 0

        for entry in data:
            fields = entry["fields"]
            name = str(fields["name"]).lower().strip()
            maker = Maker.objects.get(pk=fields["maker"])

            # Check if a monitor model with the same name already exists
            if MonitorModel.objects.filter(name=name).exists():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipped: monitor model'{name}' already exists."
                    )
                )
                continue

            # Create or update the MonitorModel instance
            monitor_model = MonitorModel.objects.create(
                pk=entry["pk"],
                name=name,
                maker=maker,
            )
            added_count += 1

            # Log output
            self.stdout.write(self.style.SUCCESS(f"Added monitor model: {name}"))

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {added_count} added, {skipped_count} skipped."
            )
        )
