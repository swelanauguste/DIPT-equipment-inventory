from django.core.management.base import BaseCommand

from ...models import User


class Command(BaseCommand):
    help = "Update technician role"

    def handle(self, *args, **kwargs):
        users = User.objects.filter(email__in=["desiree.jnbaptiste@govt.lc" ,"swelan.auguste@govt.lc"])
        for user in users:
            user.role = "technician"
            user.save()
