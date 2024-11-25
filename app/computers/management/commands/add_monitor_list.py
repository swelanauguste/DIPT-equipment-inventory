import json

from django.core.management.base import BaseCommand

from ...models import MonitorModel, Monitor


class Command(BaseCommand):
    help = "Load monitor data from JSON into the Monitor model."

    def handle(self, *args, **kwargs):
        # Load the JSON data
        with open("./static/docs/computers/monitor_list.json", "r") as file:
            data = json.load(file)

        added_count = 0
        skipped_count = 0

        for entry in data:
            fields = entry["fields"]
            serial_number = str(fields["serial_number"]).lower().strip()
            model = MonitorModel.objects.get(pk=fields["model"])
            

            # Check if a monitor with the same serial_number already exists
            if Monitor.objects.filter(serial_number=serial_number).exists():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipped: monitor'{serial_number}' already exists."
                    )
                )
                continue

            # Create or update the Monitor instance
            monitor = Monitor.objects.create(
                pk=entry["pk"],
                serial_number=serial_number,
                model=model,
                date_received=fields["date_received"],
                date_installed=fields["date_installed"],
                notes=fields["notes"],
                created_at=fields["created_at"],
                updated_at=fields["updated_at"],
            )
            added_count += 1

            # Log output
            self.stdout.write(self.style.SUCCESS(f"Added monitor model: {serial_number}"))

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {added_count} added, {skipped_count} skipped."
            )
        )
