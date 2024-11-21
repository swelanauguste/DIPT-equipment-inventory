import json

from django.core.management.base import BaseCommand

from ...models import Maker, ComputerModel


class Command(BaseCommand):
    help = "Load computer model data from JSON into the ComputerModel model."

    def handle(self, *args, **kwargs):
        # Load the JSON data
        with open("./static/docs/cm.json", "r") as file:
            data = json.load(file)

        added_count = 0
        skipped_count = 0

        for entry in data:
            fields = entry["fields"]
            name = str(fields["name"]).lower().strip()
            maker = Maker.objects.get(pk=fields["maker"])

            # Check if a computer model with the same name already exists
            if ComputerModel.objects.filter(name=name).exists():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipped: computer model'{name}' already exists."
                    )
                )
                continue

            # Create or update the ComputerModel instance
            computer_model = ComputerModel.objects.create(
                pk=entry["pk"],
                name=name,
                maker=maker,
                processor=fields["processor"],
                ram=fields["ram"],
                hdd=fields["hdd"],
            )
            added_count += 1

            # Log output
            self.stdout.write(self.style.SUCCESS(f"Added computer model: {name}"))

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {added_count} added, {skipped_count} skipped."
            )
        )
