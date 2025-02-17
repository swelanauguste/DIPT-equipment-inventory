import csv
import os
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from tickets.models import Ticket, TicketStatus


class Command(BaseCommand):
    help = "Exports ticket reports and emails them on the 1st of every month"

    def handle(self, *args, **kwargs):
        # Generate CSV file
        file_name = f"ticket_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        file_path = os.path.join(settings.MEDIA_ROOT, "reports", file_name)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure folder exists

        with open(file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["Ticket Status", "Ticket ID", "Summary", "Assigned to", "Created At"]
            )  # CSV Header

            tickets_by_status = {
                status.name: Ticket.objects.filter(ticket_status=status)
                for status in TicketStatus.objects.all()
            }

            for status, tickets in tickets_by_status.items():
                for ticket in tickets:
                    writer.writerow(
                        [
                            status,
                            ticket.ticket_id.upper(),
                            ticket.summary,
                            ticket.assigned_to,
                            ticket.created_at,
                        ]
                    )

        # Send Email with CSV Attachment
        self.send_email(file_path, file_name)

    def send_email(self, file_path, file_name):
        recipient_email = "kingship.lc@gmail.com"  # Update with actual recipient
        subject = "Monthly Ticket Report"
        body = "Attached is the monthly ticket report."

        email = EmailMessage(
            subject, body, settings.DEFAULT_FROM_EMAIL, [recipient_email, 'ict.infrastructure@govt.lc']
        )
        email.attach_file(file_path)
        email.send()

        self.stdout.write(
            self.style.SUCCESS(f"Ticket report sent successfully to {recipient_email}")
        )
