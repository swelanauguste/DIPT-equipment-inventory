from django.core.management.base import BaseCommand
from tickets.models import Ticket
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        tickets = Ticket.objects.filter(assigned_to__email="desiree.jnbaptiste@govt.lc")
        print(tickets.count())
