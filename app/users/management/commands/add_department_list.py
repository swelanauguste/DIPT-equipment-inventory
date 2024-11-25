import json

from django.core.management.base import BaseCommand

from ...models import Department


class Command(BaseCommand):
    help = "Load department data from JSON into the Department model."

    def handle(self, *args, **kwargs):
        # Load the JSON data
        with open("./static/docs/users/department_list.json", "r") as file:
            data = json.load(file)

        added_count = 0
        skipped_count = 0

        for entry in data:
            fields = entry["fields"]
            name = fields["name"]
           

            # Check if a department with the same name already exists
            if Department.objects.filter(name=name).exists():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Skipped: department'{name}' already exists.")
                )
                continue

            # Create or update the Department instance
            department = Department.objects.create(
                pk=entry["pk"],
                name=name,
            )
            added_count += 1

            # Log output
            self.stdout.write(self.style.SUCCESS(f"Added department: {name}"))

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {added_count} added, {skipped_count} skipped."
            )
        )
