from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tickets.urls")),
    path("computers/", include("computers.urls")),
    path("printers/", include("printers.urls")),
    path("users/", include("users.urls")),
]
