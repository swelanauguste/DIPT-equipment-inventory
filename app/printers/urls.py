from django.urls import path

from . import views

urlpatterns = [
    path("", views.PrinterListView.as_view(), name="printer-list"),
    path("create/", views.PrinterCreateView.as_view(), name="printer-create"),
    path(
        "detail/<slug:slug>", views.PrinterDetailView.as_view(), name="printer-detail"
    ),
    path(
        "update/<slug:slug>", views.PrinterUpdateView.as_view(), name="printer-update"
    ),
    path(
        "printer-model-list/",
        views.PrinterModelListView.as_view(),
        name="printer-model-list",
    ),
    path(
        "printer-model/create/",
        views.PrinterModelCreateView.as_view(),
        name="printer-model-create",
    ),
    path(
        "printer-model/detail/<slug:slug>",
        views.PrinterModelDetailView.as_view(),
        name="printer-model-detail",
    ),
    path(
        "printer-model/update/<slug:slug>",
        views.PrinterModelUpdateView.as_view(),
        name="printer-model-update",
    ),
]
