from django.contrib import admin

from . import models

admin.site.register(models.Ticket)
admin.site.register(models.TicketStatus)
admin.site.register(models.TicketCategory)
admin.site.register(models.Comment)

