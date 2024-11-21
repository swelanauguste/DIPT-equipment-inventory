from django.urls import path

from . import views

urlpatterns = [
    path("ticket-list/", views.TicketListView.as_view(), name="ticket-list"),
    path("detail/<slug:slug>/", views.TicketDetailView.as_view(), name="ticket-detail"),
    path(
        "update/user/<slug:slug>/",
        views.TicketUserUpdateView.as_view(),
        name="ticket-user-update",
    ),
    path(
        "update/tech/<slug:slug>/",
        views.TicketTechUpdateView.as_view(),
        name="ticket-tech-update",
    ),
    path("", views.TicketUserCreateView.as_view(), name="ticket-user-create"),
    path(
        "tech-create/",
        views.TicketTechnicianCreateView.as_view(),
        name="ticket-tech-create",
    ),
]
