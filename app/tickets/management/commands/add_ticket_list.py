import json

from django.core.management.base import BaseCommand
from users.models import User

from ...models import Ticket, TicketCategory, TicketStatus


class Command(BaseCommand):
    help = "Load ticket data from JSON into the Ticket model."

    def handle(self, *args, **kwargs):
        # Load the JSON data
        with open("./static/docs/tickets/ticket_list.json", "r") as file:
            data = json.load(file)

        added_count = 0
        skipped_count = 0

        for entry in data:
            fields = entry["fields"]
            user = fields["user"]
            ticket_id = str(fields["ticket_id"]).lower().strip()

            ticket_category = None
            if fields.get("ticket_category"):
                try:
                    ticket_category = TicketCategory.objects.get(
                        pk=fields["ticket_category"]
                    )

                except TicketCategory.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"TicketCategory with pk={fields['ticket_category']} does not exist. Skipping ticket_category."
                        )
                    )

            ticket_status = None
            if fields.get("ticket_status"):
                try:
                    ticket_status = TicketStatus.objects.get(pk=fields["ticket_status"])

                except TicketStatus.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"TicketStatus with pk={fields['ticket_status']} does not exist. Skipping ticket_status."
                        )
                    )
            assigned_to = None
            if fields.get("assigned_to"):
                try:
                    assigned_to = User.objects.get(pk=fields["assigned_to"])

                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"User with pk={fields['assigned_to']} does not exist. Skipping assigned_to."
                        )
                    )

            updated_by = None
            if fields.get("updated_by"):
                try:
                    updated_by = User.objects.get(pk=fields["updated_by"])

                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"User with pk={fields['updated_by']} does not exist. Skipping updated_by."
                        )
                    )

            # Check if a ticket with the same name already exists
            if Ticket.objects.filter(ticket_id=ticket_id).exists():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Skipped: ticket'{ticket_id}' already exists.")
                )
                continue

            # Create the Ticket instance
            ticket = Ticket.objects.create(
                pk=entry["pk"],
                ticket_id=ticket_id,
                summary=fields["summary"],
                description=fields["description"],
                ticket_status=ticket_status,
                ticket_category=ticket_category,
                assigned_to=assigned_to,
                created_at=fields["created_at"],
                updated_at=fields["updated_at"],
                updated_by=updated_by,
            )

            # Add users to the ManyToManyField
            user_ids = fields.get("user", [])
            if user_ids:  # Only proceed if user_ids is not None or empty
                if isinstance(user_ids, int):  # If it's a single integer, wrap it in a list
                    user_ids = [user_ids]

                users = User.objects.filter(pk__in=user_ids)
                ticket.user.set(users)
            
            added_count += 1

            # Log output
            self.stdout.write(self.style.SUCCESS(f"Added ticket: {ticket_id}"))

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {added_count} added, {skipped_count} skipped."
            )
        )
