from django.urls import path

from . import views

urlpatterns = [
    path("reports/", views.get_department_stats, name="reports"),
]
