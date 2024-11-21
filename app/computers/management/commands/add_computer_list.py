import json

from django.core.management.base import BaseCommand
from users.models import Department, Location, User

from ...models import Computer, ComputerModel, Monitor, OperatingSystem, Status


class Command(BaseCommand):
    help = "Load computer data from JSON into the Computer model."

    def handle(self, *args, **kwargs):
        # Load the JSON data
        with open("./static/docs/c.json", "r") as file:
            data = json.load(file)

        added_count = 0
        skipped_count = 0

        for entry in data:
            fields = entry["fields"]
            serial_number = str(fields["serial_number"]).lower().strip()
            # model = ComputerModel.objects.get(pk=fields["model"])
            status = Status.objects.get(pk=fields["status"])
            # os = OperatingSystem.objects.get(pk=fields["os"])

            # Handle optional location
            location = None
            if fields.get("location"):
                try:
                    location = Location.objects.get(pk=fields["location"])

                except Location.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Location with pk={fields['location']} does not exist. Skipping location."
                        )
                    )

            department = None
            if fields.get("department"):
                try:
                    department = Department.objects.get(pk=fields["department"])

                except Department.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Department with pk={fields['department']} does not exist. Skipping department."
                        )
                    )
            
            os = None
            if fields.get("os"):
                try:
                    os = OperatingSystem.objects.get(pk=fields["os"])

                except OperatingSystem.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"OperatingSystem with pk={fields['os']} does not exist. Skipping os."
                        )
                    )
            model = None
            if fields.get("model"):
                try:
                    model = ComputerModel.objects.get(pk=fields["model"])

                except ComputerModel.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"ComputerModel with pk={fields['model']} does not exist. Skipping model."
                        )
                    )

            # Check if a computer with the same serial_number already exists
            if Computer.objects.filter(serial_number=serial_number).exists():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipped: computer'{serial_number}' already exists."
                    )
                )
                continue

            # Create or update the Computer instance
            computer = Computer.objects.create(
                pk=entry["pk"],
                serial_number=serial_number,
                model=model,
                status=status,
                os=os,
                location=location,
                department=department,
                warranty_info=fields["warranty_info"],
                computer_name=fields["computer_name"],
                date_received=fields["date_received"],
                date_installed=fields["date_installed"],
                notes=(
                    f"{fields['notes']} (User: {fields['user']})"
                    if fields["user"]
                    else fields["notes"]
                ),
                created_at=fields["created_at"],
                updated_at=fields["updated_at"],
            )
            # Add monitors to the ManyToManyField
            if fields["monitor"]:  # Assuming "monitor" is a list of monitor PKs
                monitors = Monitor.objects.filter(
                    pk__in=fields["monitor"]
                )  # Fetch all specified monitors
                computer.monitor.set(monitors)
            added_count += 1

            # Log output
            self.stdout.write(
                self.style.SUCCESS(f"Added computer model: {serial_number}")
            )

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {added_count} added, {skipped_count} skipped."
            )
        )
