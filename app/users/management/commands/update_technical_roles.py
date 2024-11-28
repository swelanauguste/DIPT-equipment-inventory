from django.core.management.base import BaseCommand

from ...models import User


class Command(BaseCommand):
    help = "Update technical roles"

    def handle(self, *args, **kwargs):
        technicians = User.objects.filter(
            email__in=["desiree.jnbaptiste@govt.lc", "swelan.auguste@govt.lc"]
        )
        for technician in technicians:
            technician.role = "technician"
            technician.set_password('password3')
            technician.save()

            self.stdout.write(
                self.style.SUCCESS(f"Updated {technician} role to technician")
            )

        manager = User.objects.get(email="cmcclauren@gosl.gov.lc")
        manager.role = "manager"
        manager.set_password('password3')
        manager.save()
        self.stdout.write(self.style.SUCCESS(f"Updated {manager} role to manager"))
