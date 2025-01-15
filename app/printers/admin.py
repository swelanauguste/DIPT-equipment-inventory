from django.contrib import admin

from . import models

admin.site.register(models.PrinterModel)
admin.site.register(models.Printer)
admin.site.register(models.PrinterComment)