import csv
import os
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from computers.models import Computer, Status


class Command(BaseCommand):
    help = "Exports computer reports and emails them on the 1st of every month"

    def handle(self, *args, **kwargs):
        # Generate CSV file
        file_name = f"computer_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        file_path = os.path.join(settings.MEDIA_ROOT, "reports", file_name)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure folder exists

        with open(file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "status",
                    "from_project",
                    "serial_number",
                    "warranty_info",
                    "computer_name",
                    "model",
                    "monitor",
                    "os",
                    "location",
                    "department",
                    "user",
                    "date_received",
                    "date_installed",
                    "notes",
                ]
            )  # CSV Header
            
            computers_by_status = {
                status.name: Computer.objects.filter(status=status)
                for status in Status.objects.all()
            }

            for status, computers in computers_by_status.items():
                for computer in computers:
                    writer.writerow(
                        [
                            status,
                            computer.from_project,
                            computer.serial_number.upper(),
                            computer.warranty_info,
                            computer.computer_name,
                            computer.model.name.upper(),
                            computer.monitor.first(),
                            computer.os,
                            computer.location,
                            computer.department,
                            computer.user.first(),
                            computer.date_received,
                            computer.date_installed,
                            computer.notes.upper(),
                        ]
                    )

        # Send Email with CSV Attachment
        self.send_email(file_path, file_name)

    def send_email(self, file_path, file_name):
        recipient_email = "kingship.lc@gmail.com"  # Update with actual recipient
        subject = "Monthly Ticket Report"
        body = "Attached is the monthly ticket report."

        email = EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email, "ict.infrastructure@govt.lc"],
        )
        email.attach_file(file_path)
        email.send()

        self.stdout.write(
            self.style.SUCCESS(f"Ticket report sent successfully to {recipient_email}")
        )
