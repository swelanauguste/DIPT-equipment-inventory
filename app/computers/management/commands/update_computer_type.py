from django.core.management.base import BaseCommand

from ...models import ComputerModel


class Command(BaseCommand):

    def handle(self, *args, **options):
        desktop_count = 0
        laptop_count = 0
        server_count = 0

        desktops = ComputerModel.objects.filter(computer_type=1)
        for desktop in desktops:
            desktop.computer_type = "desktop"
            desktop.save()
            desktop_count += 1
            self.stdout.write(self.style.SUCCESS(f"Updates status: {desktop.name}"))

        laptops = ComputerModel.objects.filter(computer_type=2)
        for laptop in laptops:
            laptop.computer_type = "laptop"
            laptop.save()
            laptop_count += 1
            self.stdout.write(self.style.SUCCESS(f"Updates status: {laptop.name}"))

        servers = ComputerModel.objects.filter(computer_type=3)
        for server in servers:
            server.computer_type = "servers"
            server.save()
            server_count += 1
            self.stdout.write(self.style.SUCCESS(f"Updates status: {server.name}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {desktop_count} desktops updated, {laptop_count} laptops updated, servers {server_count} updated"
            )
        )
