from django.urls import path

from . import views

urlpatterns = [
    path("", views.PrinterListView.as_view(), name="device-list"),
    path("create/", views.PrinterCreateView.as_view(), name="device-create"),
    path(
        "detail/<slug:slug>/", views.PrinterDetailView.as_view(), name="device-detail"
    ),
    path(
        "update/<slug:slug>/", views.PrinterUpdateView.as_view(), name="device-update"
    ),
    path(
        "device-model-list/",
        views.PrinterModelListView.as_view(),
        name="device-model-list",
    ),
    path(
        "device-model/create/",
        views.PrinterModelCreateView.as_view(),
        name="device-model-create",
    ),
    path(
        "device-model/detail/<slug:slug>/",
        views.PrinterModelDetailView.as_view(),
        name="device-model-detail",
    ),
    path(
        "device-model/update/<slug:slug>/",
        views.PrinterModelUpdateView.as_view(),
        name="device-model-update",
    ),
    path(
        "device-comment/<slug:slug>/",
        views.add_comment_view,
        name="device-add-comment",
    ),
]
