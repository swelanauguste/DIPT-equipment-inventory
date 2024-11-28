import json

from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User

from ...models import Comment, Ticket


class Command(BaseCommand):
    help = "Load comment data from JSON into the Comment model."

    def handle(self, *args, **kwargs):
        # Load the JSON data
        with open("./static/docs/tickets/ticket_comment_list.json", "r") as file:
            data = json.load(file)

        added_count = 0
        skipped_count = 0

        for entry in data:
            fields = entry["fields"]
            ticket = Ticket.objects.get(pk=fields["ticket"])
            # created_by = fields["created_by"]
            # print(created_by)

            created_by = User.objects.get(pk=1)
            if fields.get("created_by"):
                try:
                    created_by = User.objects.get(pk=fields["created_by"])

                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"User with pk={fields['created_by']} does not exist. Skipping created_by."
                        )
                    )
            updated_at = timezone.now()
        

            # Check if a comment with the same ticket already exists
            if Comment.objects.filter(ticket=ticket).exists():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Skipped: comment'{ticket}' already exists.")
                )
                continue

            # Create or update the Comment instance
            comment = Comment.objects.create(
                pk=entry["pk"],
                ticket=ticket,
                comments=fields["comments"],
                created_at=fields["created_at"],
                created_by=created_by,
                updated_at=updated_at,
            )
            added_count += 1

            # Log output
            self.stdout.write(self.style.SUCCESS(f"Added comment: {ticket}"))

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {added_count} added, {skipped_count} skipped."
            )
        )
