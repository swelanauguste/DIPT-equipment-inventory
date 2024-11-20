import csv
from django.core.management.base import BaseCommand
from ...models import Department
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Add department list to the Department model"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path", type=str, help="Path to the file containing department list"
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        added_count = 0
        skipped_count = 0

        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 1:
                        self.stdout.write("Skipping empty row.")
                        continue
                    
                    name = row[0].strip().lower()
                    if not name:
                        self.stdout.write("Skipping row with empty name.")
                        continue
                    
                    slug = slugify(name)
                    if not Department.objects.filter(slug=slug).exists():
                        Department.objects.create(name=name, slug=slug)
                        added_count += 1
                        self.stdout.write(f"Added Department: {name}")
                    else:
                        skipped_count += 1
                        self.stdout.write(f"Skipped existing Department: {name}")

            self.stdout.write(
                self.style.SUCCESS(f"Finished! Added: {added_count}, Skipped: {skipped_count}")
            )
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {str(e)}"))
