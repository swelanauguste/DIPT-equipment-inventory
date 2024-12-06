import json
from django.core.management.base import BaseCommand
from tickets.models import Ticket, TicketCategory
from django.db import transaction

class Command(BaseCommand):
    help = "Update ticket categories to ManyToManyField"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', 
            type=str, 
            required=True, 
            help="Path to the JSON file containing ticket data."
        )

    def handle(self, *args, **options):
        file_path = options['file']
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            self.stdout.write(f"Processing {len(data)} tickets from {file_path}")

            for item in data:
                fields = item['fields']
                ticket_pk = item['pk']
                category_pk = fields.get('ticket_category')
                
                # Fetch the ticket and category
                try:
                    ticket = Ticket.objects.get(pk=ticket_pk)
                    ticket.ticket_category.clear()
                    
                    if category_pk:
                        category = TicketCategory.objects.get(pk=category_pk)
                        # Add the category to the ManyToManyField
                        ticket.ticket_category.add(category)
                        self.stdout.write(
                            f"Added category {category} to ticket {ticket.ticket_id}."
                        )
                    else:
                        self.stdout.write(
                            f"No category found for ticket {ticket.ticket_id}. Skipping."
                        )
                except Ticket.DoesNotExist:
                    self.stderr.write(f"Ticket with pk {ticket_pk} does not exist.")
                except TicketCategory.DoesNotExist:
                    self.stderr.write(f"Category with pk {category_pk} does not exist.")

            self.stdout.write("Update process completed successfully.")
        except Exception as e:
            self.stderr.write(f"Error: {e}")
