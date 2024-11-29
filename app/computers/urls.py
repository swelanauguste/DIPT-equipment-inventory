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
    path("monitor-list/", views.MonitorListView.as_view(), name="monitor-list"),
    path("monitor-create/", views.MonitorCreateView.as_view(), name="monitor-create"),
    path(
        "monitor-detail/<slug:slug>/",
        views.MonitorDetailView.as_view(),
        name="monitor-detail",
    ),
    path(
        "monitor-update/<slug:slug>/",
        views.MonitorUpdateView.as_view(),
        name="monitor-update",
    ),
    path(
        "monitor-model-list/",
        views.MonitorModelListView.as_view(),
        name="monitor-model-list",
    ),
    path(
        "create-monitor-model/",
        views.MonitorModelCreateView.as_view(),
        name="monitor-model-create",
    ),
    path(
        "monitor-model-detail/<slug:slug>/",
        views.MonitorModelDetailView.as_view(),
        name="monitor-model-detail",
    ),
    path(
        "monitor-model-update/<slug:slug>/",
        views.MonitorModelUpdateView.as_view(),
        name="monitor-model-update",
    ),
]
