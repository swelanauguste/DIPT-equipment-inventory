from django.urls import path

from . import views

urlpatterns = [
    path("", views.ComputerListView.as_view(), name="computer-list"),
    path("create/", views.ComputerCreateView.as_view(), name="computer-create"),
    path(
        "computer-detail/<slug:slug>/",
        views.ComputerDetailView.as_view(),
        name="computer-detail",
    ),
    path(
        "computer-update/<slug:slug>/",
        views.ComputerUpdateView.as_view(),
        name="computer-update",
    ),
    path(
        "computer-model-list/",
        views.ComputerModelListView.as_view(),
        name="computer-model-list",
    ),
    path(
        "create-model/",
        views.ComputerModelCreateView.as_view(),
        name="computer-model-create",
    ),
    path(
        "computer-model-detail/<slug:slug>/",
        views.ComputerModelDetailView.as_view(),
        name="computer-model-detail",
    ),
    path(
        "computer-model-update/<slug:slug>/",
        views.ComputerModelUpdateView.as_view(),
        name="computer-model-update",
    ),
]
