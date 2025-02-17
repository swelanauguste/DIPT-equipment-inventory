from django.urls import path

from . import views

urlpatterns = [
    path("reports/", views.ticket_report_view, name="reports"),
    path("reports/to_csv", views.export_tickets_to_csv, name="reports_to_csv"),
]
