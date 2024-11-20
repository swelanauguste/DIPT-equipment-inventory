from django.contrib import admin

from . import models


class ComputerAdmin(admin.ModelAdmin):
    list_display = [
        "serial_number",
        "computer_name",
        "status",
        "os",
        "location",
        "department",
    ]
    list_editable = [
        "status",
        "os",
        "location",
        "department",
    ]


admin.site.register(models.Maker)
admin.site.register(models.ComputerModel)
admin.site.register(models.Computer, ComputerAdmin)
admin.site.register(models.OperatingSystem)
admin.site.register(models.Status)
