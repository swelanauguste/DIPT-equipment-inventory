import json

from django.core.management.base import BaseCommand

from ...models import User, Department


class Command(BaseCommand):
    help = "Load user data from JSON into the User model."

    def handle(self, *args, **kwargs):
        # Load the JSON data
        with open("./static/docs/users/user_list.json", "r") as file:
            data = json.load(file)

        added_count = 0
        skipped_count = 0

        for entry in data:
            fields = entry["fields"]
            email = str(fields["email"]).lower().strip()
           

            # Check if a user with the same email already exists
            if User.objects.filter(email=email).exists():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Skipped: user '{email}' already exists.")
                )
                continue

            # Create or update the User instance
            user = User.objects.create(
                pk=entry["pk"],
                email=email,
                username=email,
                job_title=str(fields["job_title"]).lower().strip(),
                phone=fields["ext"],
                
            )
            user.set_password("Password2024"),
            user.save()
            added_count += 1

            # Log output
            self.stdout.write(self.style.SUCCESS(f"Added user: {email}"))

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {added_count} added, {skipped_count} skipped."
            )
        )
