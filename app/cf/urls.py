from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tickets/", include("tickets.urls")),
    path("computers/", include("computers.urls")),
    path("office-keys/", include("officekeys.urls")),
    path("printers/", include("printers.urls")),
    path("users/", include("users.urls")),
    path("stocks/", include("stocks.urls")),
    path("knowledge-base/", include("knowledge_base.urls")),
    path("", include("notices.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
