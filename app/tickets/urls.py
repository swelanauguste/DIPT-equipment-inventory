from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserTicketListView.as_view(), name="user-ticket-list"),
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
    path(
        "ticket-user-create",
        views.TicketUserCreateView.as_view(),
        name="ticket-user-create",
    ),
    path(
        "tech-create/",
        views.TicketTechnicianCreateView.as_view(),
        name="ticket-tech-create",
    ),
    path(
        "ticket-comment/<slug:slug>/", views.add_comment_view, name="ticket-add-comment"
    ),
    path("ticket-delete/<slug:slug>/", views.ticket_delete_view, name="ticket-delete"),
    path("ticket-reopen/<slug:slug>/", views.ticket_reopen_view, name="ticket-reopen"),
    path("ticket-close/<slug:slug>/", views.ticket_close_view, name="ticket-close"),
]
