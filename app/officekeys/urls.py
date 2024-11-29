from django.urls import path

from . import views

urlpatterns = [
    path(
        "microsoft-office-list/",
        views.MicrosoftOfficeListView.as_view(),
        name="microsoft-office-list",
    ),
  
    path(
        "microsoft-office-create/",
        views.MicrosoftOfficeCreateView.as_view(),
        name="microsoft-office-create",
    ),
    path(
        "microsoft-office-detail/<int:pk>/",
        views.MicrosoftOfficeDetailView.as_view(),
        name="microsoft-office-detail",
    ),
    path(
        "microsoft-office-update/<int:pk>/",
        views.MicrosoftOfficeUpdateView.as_view(),
        name="microsoft-office-update",
    ),
    path(
        "microsoft-office-assign/<int:pk>/",
        views.MicrosoftOfficeAssignView.as_view(),
        name="microsoft-office-assign",
    ),
    path(
        "microsoft-office-assign-list/",
        views.MicrosoftOfficeAssignListView.as_view(),
        name="microsoft-office-assign-list",
    ),
    path(
        "microsoft-office-assign-detail/<int:pk>/",
        views.MicrosoftOfficeAssignDetailView.as_view(),
        name="microsoft-office-assignment-detail",
    ),
    path(
        "microsoft-office-assign-update/<int:pk>/",
        views.MicrosoftOfficeAssignUpdateView.as_view(),
        name="microsoft-office-assignment-update",
    ),
]


