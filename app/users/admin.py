from django.contrib import admin

from .models import Department, Location, User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "role",
        "location",
        "department",
    ]
    list_editable = ["role", "location", "department"]


admin.site.register(User, UserAdmin)
admin.site.register(Department)
admin.site.register(Location)
