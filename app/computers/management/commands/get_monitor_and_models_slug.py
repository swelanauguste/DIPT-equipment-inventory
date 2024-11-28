from django.core.management.base import BaseCommand
from ...models import Monitor, MonitorModel


class Command(BaseCommand):

    def handle(self, *args, **options):

        monitors = Monitor.objects.all()
        for monitor in monitors:
            monitor.save()

        monitor_models = MonitorModel.objects.all()
        for monitor_model in monitor_models:
            monitor_model.save()
