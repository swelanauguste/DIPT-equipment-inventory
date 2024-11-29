from django.core.management.base import BaseCommand
from printers.models import Printer, PrinterModel


class Command(BaseCommand):

    def handle(self, *args, **options):

        printers = Printer.objects.all()
        for printer in printers:
            printer.save()

        printer_models = PrinterModel.objects.all()
        for printer_model in printer_models:
            printer_model.save()
